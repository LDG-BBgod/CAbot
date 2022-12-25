from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.core import serializers

from .forms import ConsultingForm
from .models import ChatRoomName, ChatLog, Consulting
from .apis import sendMessageFunc

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

    
    try:
        chatLogs = ChatLog.objects.filter(chatRoomNameObject = ChatRoomName.objects.get(userIP=userIP))

    except:
        return redirect('/caHome/')
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

def SelfCompareHomeView(request):

    return render(request, 'selfCompareHome.html')





# API

def SendMessageAPI(request):
    
    dataType = request.GET.get('dataType')
    if dataType == 'consulting':
        selectType = request.GET.get('selectType')
        phone = request.GET.get('phone')
        consultingDate = request.GET.get('consultingDate')
        consultingTime = request.GET.get('consultingTime')
        content = '카봇\n상담수단 : ' + selectType + '\n연락처 : ' + phone + '\n상담 시간 : ' + consultingDate + ' ' +  consultingTime
    
    sendMessageFunc(content)

    return HttpResponse()





# 추가페이지

def CompanyView(request):
    
    return render(request, 'addCompany.html')

def AgreementView(request):
    
    return render(request, 'addAgreement.html')





