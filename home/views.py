from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.core import serializers

from .forms import ConsultingForm
from .models import ChatRoomName, ChatLog, Consulting

import hashlib, hmac, base64, time
import requests, json


def HomeView(request):

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    userIP = get_client_ip(request)
    request.session['user'] = userIP

    response = render(request, 'home.html', {'userIP': userIP})
    response.set_cookie(key='user', value='user')

    return response


def CAHomeView(request):

    chatRoomNames = ChatRoomName.objects.all()

    return render(request, 'caHome.html', {'chatRoomNames': chatRoomNames})


def CAChatView(request, userIP):

    chatLogs = ChatLog.objects.filter(chatRoomNameObject = ChatRoomName.objects.get(userIP=userIP))
    
    contents = {
        'userIP': userIP,
        'chatLogs': chatLogs,
    }

    response = render(request, 'caChat.html', contents)
    response.set_cookie(key='user', value='LDJ')

    return response


class ConsultingView(FormView):
    template_name = 'consulting.html'
    form_class = ConsultingForm
    success_url = '/'

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


def ConsultingDataView(request):
    data = request.GET.get('data')
    consultingObject = Consulting.objects.filter(consultingDate=data)
    responseData = serializers.serialize('json', consultingObject)

    return HttpResponse(responseData, content_type="text/json-comment-filtered")




# API

def SendMessageAPI(request):
    
    dataType = request.GET.get('dataType')
    if dataType == 'consulting':
        selectType = request.GET.get('selectType')
        phone = request.GET.get('phone')
        consultingDate = request.GET.get('consultingDate')
        consultingTime = request.GET.get('consultingTime')
        content = '카봇\n상담수단 : ' + selectType + '\n연락처 : ' + phone + '\n상담 시간 : ' + consultingDate + ' ' +  consultingTime
        
    def getSigningKey():

        timestamp = str(int(time.time() * 1000))

        access_key = "Lyf4UlLYnAqvptuxG9Oq"
        secret_key = "O8DxN19g9zaRZ335Wgx5FCzQfXPIbZfkLR5dng4C"
        secret_key = bytes(secret_key, 'UTF-8')

        method = "POST"
        
        uri = "/sms/v2/services/ncp:sms:kr:289661419957:gabot/messages"

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey
 

    headers = {
        "Contenc-type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": str(int(time.time() * 1000)),
        "x-ncp-iam-access-key": 'Lyf4UlLYnAqvptuxG9Oq',
        "x-ncp-apigw-signature-v2": getSigningKey(),
        }
    body = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': '01054088229',
        'content': content,
        'messages': [{
            'to': '01050487229',
        }],
    }
    res = requests.post('https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:289661419957:gabot/messages', json=body, headers=headers)
    
    return HttpResponse()


# 추가페이지

def CompanyView(request):
    
    return render(request, 'addCompany.html')

def AgreementView(request):
    
    return render(request, 'addAgreement.html')





