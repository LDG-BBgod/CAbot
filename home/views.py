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
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import subprocess

from datetime import date, timedelta



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
    
    # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
    # options.add_argument('user-agent=' + user_agent)  
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    options = Options()

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
    options.add_argument("disable-gpu")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)


    



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

import random

def selfCompareAPICarMaker(request):

    # content = {}

    # userIP = request.session.get('user')
    # browser = browsers[userIP]

    # trigger = True
    # while trigger:
    #     try:
    #         browser.find_element(By.CSS_SELECTOR, '#newcar_title_1').send_keys(Keys.ENTER)
    #         browser.implicitly_wait(5)
    #         time.sleep(0.2)
    #         trigger = False

    #     except:
    #         pass

    # optionUL = browser.find_element(By.CSS_SELECTOR, '#dMaker > ul')
    # optionLIs = optionUL.find_elements(By.TAG_NAME, 'input')
    
    # for optionLI in optionLIs:

    #     content[optionLI.get_attribute('id')] = optionLI.get_attribute('value')

    # return HttpResponse(json.dumps(content))
    

    userIP = request.session.get('user')
    browser = browsers[userIP]

    content = {}
    carMakerUL = browser.find_element(By.CSS_SELECTOR, '#dMaker > ul')
    carMakerLIs = carMakerUL.find_elements(By.TAG_NAME, 'li')

    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    for carMakerLI in carMakerLIs:

        a += 1
        b = 0
        c = 0
        d = 0
        e = 0


        trigger1_1 = True
        while trigger1_1:
            try:
                time.sleep(0.4)
                carMakerInput = carMakerLI.find_element(By.TAG_NAME, 'input')
                carMakerLabel = carMakerLI.find_element(By.TAG_NAME, 'label')
                browser.find_element(By.CSS_SELECTOR, '#newcar_title_1').send_keys(Keys.ENTER)
                browser.implicitly_wait(5)
                makerInputID = carMakerInput.get_attribute('id')
                trigger1_1 = False
            except StaleElementReferenceException:
                print('s트리거1_1')
                time.sleep(0.1)
            except ElementNotInteractableException:
                print('e트리거1_1')
                time.sleep(0.1)

        content[makerInputID] = []
        content[makerInputID].append(carMakerLabel.text)
        content[makerInputID].append({})

        trigger1_2 = True
        while trigger1_2:
            try:
                time.sleep(0.4)
                carMakerInput.click()
                browser.implicitly_wait(5)
                trigger1_2 = False
            except StaleElementReferenceException:
                print('s트리거1_2')
                time.sleep(0.1)
            except ElementNotInteractableException:
                print('e트리거1_2')
                time.sleep(0.1)

        trigger1_3 = True
        while trigger1_3:
            try:
                carNameUL = browser.find_element(By.CSS_SELECTOR, '#dCarName > ul')
                carNameLIs = carNameUL.find_elements(By.TAG_NAME, 'li')
                trigger1_3 = False
            except StaleElementReferenceException:
                print('s트리거1_3')
                time.sleep(0.1)
            except ElementNotInteractableException:
                print('e트리거1_3')
                time.sleep(0.1)

        for carNameLI in carNameLIs:

            b += 1
            c = 0
            d = 0
            e = 0

            trigger2_1 = True
            while trigger2_1:
                try:
                    time.sleep(0.4)
                    carNameInput = carNameLI.find_element(By.TAG_NAME, 'input')
                    carNameLabel = carNameLI.find_element(By.TAG_NAME, 'label')
                    browser.find_element(By.CSS_SELECTOR, '#newcar_title_2').send_keys(Keys.ENTER)
                    browser.implicitly_wait(5)
                    NameInputID = carNameInput.get_attribute('id')
                    trigger2_1 = False
                    
                except StaleElementReferenceException:
                    print('s트리거2_1')
                    time.sleep(0.1)
                except ElementNotInteractableException:
                    print('e트리거2_1')
                    time.sleep(0.1)

            
            content[makerInputID][1][NameInputID] = []
            content[makerInputID][1][NameInputID].append(carNameLabel.text)
            content[makerInputID][1][NameInputID].append({})

            trigger2_2 = True
            while trigger2_2:
                try:
                    time.sleep(0.4)
                    carNameInput.click()
                    browser.implicitly_wait(5)
                    trigger2_2 = False
                except StaleElementReferenceException:
                    print('s트리거2_2')
                    time.sleep(0.1)
                except ElementNotInteractableException:
                    print('e트리거2_2')
                    time.sleep(0.1)

            trigger2_3 = True
            while trigger2_3:
                try:
                    carRegisterUL = browser.find_element(By.CSS_SELECTOR, '#dMadeym > ul')
                    carRegisterLIs = carRegisterUL.find_elements(By.TAG_NAME, 'li')
                    trigger2_3 = False
                except StaleElementReferenceException:
                    print('s트리거2_3')
                    time.sleep(0.1)
                except ElementNotInteractableException:
                    print('e트리거2_3')
                    time.sleep(0.1)
                    
            print(f'진행도 {a}.{b}.{c}.{d}.{e}')


        #     for carRegisterLI in carRegisterLIs:

        #         c += 1
        #         d = 0
        #         e = 0

        #         trigger3_1 = True
        #         while trigger3_1:
        #             try:
        #                 time.sleep(0.4)
        #                 carRegisterInput = carRegisterLI.find_element(By.TAG_NAME, 'input')
        #                 carRegisterLabel = carRegisterLI.find_element(By.TAG_NAME, 'label')
        #                 browser.find_element(By.CSS_SELECTOR, '#newcar_title_3').send_keys(Keys.ENTER)
        #                 browser.implicitly_wait(5)
        #                 RegisterInputID = carRegisterInput.get_attribute('id')
        #                 trigger3_1 = False
        #             except StaleElementReferenceException:
        #                 print('s트리거3_1')
        #                 time.sleep(0.1)
        #             except ElementNotInteractableException:
        #                 print('e트리거3_1')
        #                 time.sleep(0.1)

                
        #         content[makerInputID][1][NameInputID][1][RegisterInputID] = []
        #         content[makerInputID][1][NameInputID][1][RegisterInputID].append(carRegisterLabel.text)
        #         content[makerInputID][1][NameInputID][1][RegisterInputID].append({})


        #         trigger3_2 = True
        #         while trigger3_2:
        #             try:
        #                 time.sleep(0.4)
        #                 carRegisterInput.click()
        #                 browser.implicitly_wait(5)
        #                 trigger3_2 = False
        #             except StaleElementReferenceException:
        #                 print('s트리거3_2')
        #                 time.sleep(0.1)
        #             except ElementNotInteractableException:
        #                 print('e트리거3_2')
        #                 time.sleep(0.1)

        #         trigger3_3 = True
        #         while trigger3_3:
        #             try:
        #                 carSubNameUL = browser.find_element(By.CSS_SELECTOR, '#dCarNameDtl > ul')
        #                 carSubNameLIs = carSubNameUL.find_elements(By.TAG_NAME, 'li')
        #                 trigger3_3 = False
        #             except StaleElementReferenceException:
        #                 print('s트리거3_3')
        #                 time.sleep(0.1)
        #             except ElementNotInteractableException:
        #                 print('e트리거3_3')
        #                 time.sleep(0.1)


        #         for carSubNameLI in carSubNameLIs:

        #             d += 1
        #             e = 0

        #             trigger4_1 = True
        #             while trigger4_1:
        #                 try:
        #                     time.sleep(0.4)
        #                     carSubNameInput = carSubNameLI.find_element(By.TAG_NAME, 'input')
        #                     carSubNameLabel = carSubNameLI.find_element(By.TAG_NAME, 'label')
        #                     browser.find_element(By.CSS_SELECTOR, '#newcar_title_4').send_keys(Keys.ENTER)
        #                     browser.implicitly_wait(5)
        #                     SubNameInputID = carSubNameInput.get_attribute('id')
        #                     trigger4_1 = False
        #                 except StaleElementReferenceException:
        #                     print('s트리거4_1')
        #                     time.sleep(0.1)
        #                 except ElementNotInteractableException:
        #                     print('e트리거4_1')
        #                     time.sleep(0.1)

        #             content[makerInputID][1][NameInputID][1][RegisterInputID][1][SubNameInputID] = []
        #             content[makerInputID][1][NameInputID][1][RegisterInputID][1][SubNameInputID].append(carSubNameLabel.text)
        #             content[makerInputID][1][NameInputID][1][RegisterInputID][1][SubNameInputID].append({})

        #             trigger4_2 = True
        #             while trigger4_2:
        #                 try:
        #                     time.sleep(0.4)
        #                     carSubNameInput.click()
        #                     browser.implicitly_wait(5)
        #                     trigger4_2 = False
        #                 except StaleElementReferenceException:
        #                     print('s트리거4_2')
        #                     time.sleep(0.1)
        #                 except ElementNotInteractableException:
        #                     print('e트리거4_2')
        #                     time.sleep(0.1)

        #             trigger4_3 = True
        #             while trigger4_3:
        #                 try:
        #                     carOptionUL = browser.find_element(By.CSS_SELECTOR, '#dOptionDtl > ul')
        #                     carOptionLIs = carOptionUL.find_elements(By.TAG_NAME, 'li')
        #                     trigger4_3 = False
        #                 except StaleElementReferenceException:
        #                     print('s트리거4_3')
        #                     time.sleep(0.1)
        #                 except ElementNotInteractableException:
        #                     print('e트리거4_3')
        #                     time.sleep(0.1)


        #             for carOptionLI in carOptionLIs:
        #                 time.sleep(1)
        #                 e += 1

        #                 trigger5_1 = True
        #                 while trigger5_1:
        #                     try:
        #                         print(carOptionLI)
        #                         carOptionInput = carOptionLI.find_element(By.TAG_NAME, 'input')
        #                         carOptionLabel = carOptionLI.find_element(By.TAG_NAME, 'label')
        #                         OptionInputID = carOptionInput.get_attribute('id')
        #                         trigger5_1 = False
        #                     except StaleElementReferenceException:
        #                         print('s트리거5_1')
        #                         time.sleep(0.1)
        #                     except ElementNotInteractableException:
        #                         print('e트리거5_1')
        #                         time.sleep(0.1)

        #                 content[makerInputID][1][NameInputID][1][RegisterInputID][1][SubNameInputID][1][OptionInputID] = []
        #                 content[makerInputID][1][NameInputID][1][RegisterInputID][1][SubNameInputID][1][OptionInputID].append(carOptionLabel.text)
        #                 print(f'진행도 {a}.{b}.{c}.{d}.{e}')



    with open('test.json', 'w', encoding='UTF-8') as outfile:
        json.dump(content, outfile, ensure_ascii=False, indent=2)


    return HttpResponse(json.dumps({}))


def selfCompareAPICarName(request):

    content = {}

    userIP = request.session.get('user')
    browser = browsers[userIP]
    labelID = request.GET.get('id')

    print(labelID)
    browser.find_element(By.CSS_SELECTOR, f'#{labelID}').click()
    browser.implicitly_wait(5)

    time.sleep(0.2)

    optionUL = browser.find_element(By.CSS_SELECTOR, '#dCarName > ul')
    optionLIs = optionUL.find_elements(By.TAG_NAME, 'input')

    for optionLI in optionLIs:

        content[optionLI.get_attribute('id')] = optionLI.get_attribute('value')

    return HttpResponse(json.dumps(content))


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


@superUser_required
def CADataView(request):

    caObjects = [{
        'registerDate': date.today(),
        'query': CAUser.objects.filter(registerDate__range=[date.today(), date.today() + timedelta(days=1)])
    }]

    for i in range(59):

        caObjects.append({
            'registerDate': date.today() - timedelta(days=i+1),
            'query': CAUser.objects.filter(registerDate__range=[date.today() - timedelta(days=i+1), date.today() - timedelta(days=i)])
        })

    contents = {
        'data': []
    }

    for caObject in caObjects:

        selfCompareCount = 0

        for obj in caObject['query']:
            if obj.selfCompareCount != 0:
                selfCompareCount += 1

        contents['data'].append({
            'registerDate': caObject['registerDate'],
            'visitCount': caObject['query'].count(),
            'selfCompareCount': selfCompareCount
        })

    return render(request, 'caData.html', contents)


# 추가페이지

def CompanyView(request):
    
    return render(request, 'addCompany.html')

def AgreementView(request):
    
    return render(request, 'addAgreement.html')
