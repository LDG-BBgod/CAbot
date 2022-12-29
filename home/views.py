from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


from .forms import ConsultingForm
from .models import ChatRoomName, ChatLog, Consulting, CAUser
from .apis import sendMessageFunc
from .decorators import superUser_required

import hashlib, hmac, base64, time
import requests, json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
import subprocess


def HomeView(request):

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    try:
        userIP = CAUser.objects.get(userIP = get_client_ip(request))
        userIP.homeCount += 1
        userIP.save()
        request.session['user'] = userIP.userIP

    except CAUser.DoesNotExist:
        userIP = CAUser(userIP = get_client_ip(request))
        userIP.save()
        request.session['user'] = userIP.userIP


    response = render(request, 'home.html', {'userIP': userIP})
    response.set_cookie(key='user', value='user')

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

    def render_to_response(self, context, **response_kwargs):
        response = super(ConsultingView, self).render_to_response(context, **response_kwargs)
        response.set_cookie(key='user', value='LDJ')
        return response


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['userIP'] = self.request.session['user']
        return context


def ConsultingDataView(request):
    data = request.GET.get('data')
    consultingObject = Consulting.objects.filter(consultingDate=data)
    responseData = serializers.serialize('json', consultingObject)

    return HttpResponse(responseData, content_type="text/json-comment-filtered")

def SelfCompareHomeView(request):

    response = render(request, 'selfCompareHome.html')
    response.set_cookie(key='user', value='user')

    return response



def SelfCompareStep1View(request):

    response = render(request, 'selfCompareStep1.html')
    response.set_cookie(key='user', value='user')

    return response









# API
def UserCountAPI(request):

    data = request.GET.get('data')
    userIP = request.session.get('user')
    caUser = CAUser.objects.filter(userIP=userIP).first()

    if data == 'selfCompareCount':
        caUser.selfCompareCount += 1
        caUser.save()
    elif data == 'consultingCount':
        caUser.consultingCount += 1
        caUser.save()
    elif data == 'chatCount':
        caUser.chatCount += 1
        caUser.save()

    return HttpResponse()


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


browsers = {}
def selfCompareAPIInit(request):

    userIP = request.session.get('user')

    options = webdriver.ChromeOptions()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    options.add_argument('user-agent=' + user_agent)

    # options.add_argument("disable-gpu")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)
    

    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
    options.add_experimental_option("debuggerAddress", "127.0.0.2:9222")

    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # options.add_experimental_option("detach", True)


    browsers[userIP] = webdriver.Chrome('./chromedriver_108.exe', options=options)
    browser = browsers[userIP]
    browser.implicitly_wait(5)
    browser.maximize_window()

    browser.get('https://www.e-insmarket.or.kr/')
    browser.implicitly_wait(5)
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR, '#slick-slide00 > div > div > div > a').send_keys(Keys.ENTER)
    browser.implicitly_wait(5)


    browser.find_element(By.CSS_SELECTOR, '#allTermAgreeButton').send_keys(Keys.ENTER)
    time.sleep(0.2)
    browser.find_element(By.CSS_SELECTOR, '#story3_btn > button.mobile').send_keys(Keys.ENTER)
    browser.implicitly_wait(5)
    time.sleep(0.2)
    browser.find_element(By.CSS_SELECTOR, '#authInfo > div.terms > button').send_keys(Keys.ENTER)
    time.sleep(0.2)
    browser.find_element(By.CSS_SELECTOR, '#agreeChk5').click()
    time.sleep(0.2)

    return HttpResponse(json.dumps({}))


def selfCompareAPIStep1(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    # userName = request.GET.get('userName')
    # gender = request.GET.get('gender')
    # foreigner = request.GET.get('foreigner')
    # ssmFront = request.GET.get('ssmFront')
    # ssmBack = request.GET.get('ssmBack')
    # agency = request.GET.get('agency')
    # phone1 = request.GET.get('phone1')
    # phone2 = request.GET.get('phone2')
    # phone3 = request.GET.get('phone3')

    userName = '이동권'
    gender = 'male'
    foreigner = '내국인'
    ssmFront = '960527'
    ssmBack = '1157812'
    agency = 'lg+'
    phone1 = '010'
    phone2 = '5408'
    phone3 = '8229'


    browser.find_element(By.ID, 'name').send_keys(userName)
    time.sleep(0.2)
    browser.find_element(By.NAME, 'jumin1').send_keys(ssmFront)
    time.sleep(0.2)
    browser.find_element(By.NAME, 'jumin2').send_keys(ssmBack)
    time.sleep(0.2)
    browser.find_element(By.NAME, 'phoneNum2').send_keys(phone2)
    time.sleep(0.2)
    browser.find_element(By.NAME, 'phoneNum3').send_keys(phone3)
    time.sleep(0.2)

    if gender == 'male':
        browser.find_element(By.CSS_SELECTOR, '#sexM').click()
        
    else:
        browser.find_element(By.CSS_SELECTOR, '#sexF').click()

    time.sleep(0.2)

    if foreigner == '내국인':
        browser.execute_script("""$('select[name="localDiv"]').val('1').prop('selected', true)""")
    else:
        browser.execute_script("""$('select[name="localDiv"]').val('2').prop('selected', true)""")
    
    time.sleep(0.2)

    if agency == 'skt':
        browser.find_element(By.CSS_SELECTOR, '#aSkt').click()
    elif agency == 'kt':
        browser.find_element(By.CSS_SELECTOR, '#aKt').click()
    elif agency == 'lg':
        browser.find_element(By.CSS_SELECTOR, '#aLg').click()
    elif agency == 'skt+':
        browser.find_element(By.CSS_SELECTOR, '#arSkt').click()
    elif agency == 'kt+':
        browser.find_element(By.CSS_SELECTOR, '#arKt').click()
    else:
        browser.find_element(By.CSS_SELECTOR, '#arLg').click()

    time.sleep(0.2)

    if phone1 == '010':
        browser.execute_script("""$('select[name="phoneNum1"]').val('010').prop('selected', true)""")
    elif phone1 == '011':
        browser.execute_script("""$('select[name="phoneNum1"]').val('011').prop('selected', true)""")
    elif phone1 == '016':
        browser.execute_script("""$('select[name="phoneNum1"]').val('016').prop('selected', true)""")
    elif phone1 == '017':
        browser.execute_script("""$('select[name="phoneNum1"]').val('017').prop('selected', true)""")
    elif phone1 == '018':
        browser.execute_script("""$('select[name="phoneNum1"]').val('018').prop('selected', true)""")
    elif phone1 == '019':
        browser.execute_script("""$('select[name="phoneNum1"]').val('019').prop('selected', true)""")

    time.sleep(0.2)

    trigger = True
    while trigger:

        try:
            browser.find_element(By.CSS_SELECTOR, '#authInfo > div.btn_set > button:nth-child(2)').send_keys(Keys.ENTER)
            browser.implicitly_wait(2)
            time.sleep(0.2)
            browser.find_element(By.CSS_SELECTOR, '#authNo > div > ul > li:nth-child(1) > button')
            trigger = False

        except NoSuchElementException:
            browser.find_element(By.CSS_SELECTOR, '#authInfo > div.btn_set > button:nth-child(2)').send_keys(Keys.ESCAPE)
            browser.implicitly_wait(1)
            time.sleep(0.2)

    return HttpResponse(json.dumps({}))


def selfCompareAPIStep2(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    authNum = request.GET.get('authNum')

    browser.find_element(By.ID, 'authNumber').clear()
    browser.find_element(By.ID, 'authNumber').send_keys(authNum)
    browser.find_element(By.CSS_SELECTOR, '#authNo > div > ul > li:nth-child(1) > button').send_keys(Keys.ENTER)
    browser.implicitly_wait(10)
    time.sleep(0.2)

    try:
        browser.find_element(By.CSS_SELECTOR, '#ifArea > div.con02_story.con_new > div.inq_before > div.insub_btn > a')
    
    except NoSuchElementException:
        browser.find_element(By.CSS_SELECTOR, '#authInfo > div.btn_set > button:nth-child(2)').send_keys(Keys.ESCAPE)

        return HttpResponse(json.dumps({'result': 'fail'}))


    return HttpResponse(json.dumps({'result': 'success'}))


def selfCompareAPIStep3(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    nowDate = request.GET.get('nowDate')
    nextDate = request.GET.get('nextDate')

    browser.find_element(By.CSS_SELECTOR, '#ifArea > div.con02_story.con_new > div.inq_before > div.insub_btn > a').send_keys(Keys.ENTER)
    browser.implicitly_wait(5)

    trigger = True
    while trigger:
        try:
            sendButton = browser.find_element(By.CSS_SELECTOR, '#newcar > div.con02_story.con_new.active > div.inq_after > div.insub_btn > a')
            time.sleep(0.2)
            trigger = False
        except:
            pass

    browser.execute_script(f"""
        document.getElementById('insStartDtPicker').value = "{nowDate}";
        document.getElementById('datepicker2').value = "{nextDate}";
    """)
    time.sleep(0.2)
    sendButton.send_keys(Keys.ENTER)
    browser.implicitly_wait(5)

    return HttpResponse(json.dumps({}))

def selfCompareAPIStep4(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    return HttpResponse()


def selfCompareAPICarMaker(request):

    content = {}

    userIP = request.session.get('user')
    browser = browsers[userIP]

    trigger = True
    while trigger:
        try:
            browser.find_element(By.CSS_SELECTOR, '#newcar_title_1').send_keys(Keys.ENTER)
            browser.implicitly_wait(5)
            time.sleep(0.2)
            trigger = False

        except:
            pass

    optionUL = browser.find_element(By.CSS_SELECTOR, '#dMaker > ul')
    optionLIs = optionUL.find_elements(By.TAG_NAME, 'input')
    
    for optionLI in optionLIs:

        content[optionLI.get_attribute('id')] = optionLI.get_attribute('value')

    return HttpResponse(json.dumps(content))


def selfCompareAPICarName(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    return HttpResponse()


def selfCompareAPICarRegister(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    return HttpResponse()


def selfCompareAPICarSubName(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    return HttpResponse()


def selfCompareAPICarOption(request):

    userIP = request.session.get('user')
    browser = browsers[userIP]

    return HttpResponse()







# 추가페이지

def CompanyView(request):
    
    return render(request, 'addCompany.html')

def AgreementView(request):
    
    return render(request, 'addAgreement.html')



# 관리자 페이지
def CALoginView(request):

    if request.session.get('superUser'):
        return redirect('/caHome/')

    if request.method == 'POST':

        if request.POST.get('userid') != User.objects.last().username:

            return render(request, 'caLogin.html', {'error': '아이디가 잘못되었습니다.'})
        if not check_password(request.POST.get('userpw'), User.objects.last().password):

            return render(request, 'caLogin.html', {'error': '비밀번호가 잘못되었습니다.'})

        request.session['superUser'] = request.POST.get('userid')
        
        return redirect('/caHome/')

    return render(request, 'caLogin.html')

def CALogoutView(request):

    if request.session.get('superUser'):
        del(request.session['superUser'])

    return redirect('/')


@superUser_required
def CAHomeView(request):

    chatRoomNames = ChatRoomName.objects.all()

    return render(request, 'caHome.html', {'chatRoomNames': chatRoomNames})


@superUser_required
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





