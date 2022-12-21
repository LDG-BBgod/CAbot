import json
from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async
from home.models import ChatRoomName, ChatLog
from home.apis import sendMessageFunc


@sync_to_async
def save_chatRoomName(userIP):

    try:
        chatRoomName = ChatRoomName.objects.get(userIP = userIP)

    except ChatRoomName.DoesNotExist:
        chatRoomName = ChatRoomName(userIP = userIP)
        chatRoomName.save()


@sync_to_async
def del_chatRoomName(userIP):

    chatRoomName = ChatRoomName.objects.get(userIP=userIP)

    return chatRoomName.delete()


@sync_to_async
def get_object(userIP):

    return ChatRoomName.objects.get(userIP=userIP)


@sync_to_async
def save_log(chatRoomNameObject, username, log):
    log = ChatLog(
        chatRoomNameObject = chatRoomNameObject,
        username = username,
        log = log
    )
    log.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

    	# 파라미터 값으로 채팅 룸을 구별
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 룸 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await save_chatRoomName(self.room_name)

        messages = ['안녕하세요! 보험비서 카봇입니다.', '실시간 채팅서비스 이용 가능시간은 평일 10:00 ~ 18:00 입니다.', '질문을 입력해주세요.']
        for i in range(3):
            await self.send(text_data=json.dumps({
                'message': messages[i],
                'username': 'Admin',
            }))

    async def disconnect(self, close_code):

        user = self.scope['cookies']['user']

        if (user == 'user'):
            await del_chatRoomName(self.room_name)

        # 룸 그룹 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        try:
            connectCheck = text_data_json['connectCheck']
            messages = ['채팅상담원이 연결되고있습니다. 잠시만 기다려주세요.(최대 1분)', '연결중...']
            
            content = '카봇 실시간채팅상담\n유저아이피 : ' + username
            sendMessageFunc(content)
            
            for i in range(2):
                await self.send(text_data=json.dumps({
                    'message': messages[i],
                    'username': 'Admin',
                }))

        except:
            pass

        try:
            mType = text_data_json['type']
            await self.send(text_data=json.dumps({
                'message': '죄송합니다. 현재 상담접수량이 많아 대응이 어렵습니다.  전화상담을 이용해주세요. 광고 영업 일절 없습니다.',
                'username': 'Admin',
                }))
        except:
            pass
        
        chatRoomNameObject = await get_object(self.room_name)
        await save_log(chatRoomNameObject, username, message)

        # 룸 그룹으로 메세지 보냄
        await self.channel_layer.group_send(
                      
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # 룸 그룹으로부터 메세지 받음
    async def chat_message(self, event):

        message = event['message']
        username = event['username']

        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))