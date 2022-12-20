from django.db import models


class ChatRoomName(models.Model):
    userIP = models.CharField(max_length=64, verbose_name='유저IP', default='유저IP')
    registerDate = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.userIP

    class Meta:
        db_table = 'home_chatRoomName'
        verbose_name = '채팅방이름'
        verbose_name_plural = '채팅방이름'

class ChatLog(models.Model):
    chatRoomNameObject = models.ForeignKey('home.ChatRoomName', on_delete=models.CASCADE, verbose_name='채팅방이름')
    username = models.CharField(max_length=64, verbose_name='유저이름')
    log = models.TextField(verbose_name='채팅로그')
    registerDate = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    class Meta:
        db_table = 'home_chatLog'
        verbose_name = '채팅로그'
        verbose_name_plural = '채팅로그'