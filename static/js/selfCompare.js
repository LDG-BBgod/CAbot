window.onload = () => {

    $.ajax({
        type: 'GET',
        url: '/selfCompareAPIInit/',
        dataType: 'json',
        data: {},
        success: function(request) {

        }
    })
}


var today = new Date()
var year = today.getFullYear();
var month = ('0' + (today.getMonth() + 1)).slice(-2)
var day = ('0' + today.getDate()).slice(-2)
var dateString = year + '-' + month  + '-' + day

var nextDay = new Date(today.setFullYear(today.getFullYear() + 1))
var nextYear = nextDay.getFullYear();
var nextMonth = ('0' + (nextDay.getMonth() + 1)).slice(-2)
var nextDay = ('0' + nextDay.getDate()).slice(-2)
var nextDateString = nextYear + '-' + nextMonth  + '-' + nextDay

document.getElementById('nowDate').value = dateString
document.getElementById('nextDate').value = nextDateString


//스탭1 함수

function SendAuth() {
    userName = $('#userName').val()
    gender = $("input[name='gender']:checked").val()
    foreigner = $("#foreigner option:selected").val()
    ssmFront = $("#ssmFront").val()
    ssmBack = $("#ssmBack").val()
    agency = $("input[name='phone']:checked").val()
    phone1 = $("#phone1").val()
    phone2 = $("#phone2").val()
    phone3 = $("#phone3").val()

    $('#mask, #loadingImg').show()

    new Promise((resolve) => {
        $.ajax({
            type: 'GET',
            url: '/selfCompareAPIStep1/',
            dataType: 'json',
            data: {
                'userName': userName,
                'gender': gender,
                'foreigner': foreigner,
                'ssmFront': ssmFront,
                'ssmBack': ssmBack,
                'agency': agency,
                'phone1': phone1,
                'phone2': phone2,
                'phone3': phone3,
            },
            success: function(request) {
                $('#mask, #loadingImg').hide()
                $('#sectionAuth').show()
                resolve()
            }
        })
    })
}



function AuthSubmit() {

    authNum = $('#authNum').val()

    $('#mask, #loadingImg').show()

    new Promise((resolve) => {
        $.ajax({
            type: 'GET',
            url: '/selfCompareAPIStep2/',
            dataType: 'json',
            data: {
                'authNum': authNum,
            },
            success: function(request) {
                $('#mask, #loadingImg').hide()

                if (request.result == 'fail') {
                    alert('인증번호를 확인해주세요.')
                }
                else {
                    $('.step1').hide()
                    $('.step2').show()
                }
                resolve()
            }
        })
    })
    
}


//스탭2 함수


function ChangeNextDate() {
    const nowDate = document.getElementById('nowDate').value
    var nowDateArr = Array.from(nowDate)

    nowDateArr[3] = String(Number(nowDateArr[3]) + 1)

    var nowDateStr = nowDateArr.join('')
    
    document.getElementById('nextDate').value = nowDateStr
}


function ChangeStep2Section() {

    const nowDate = document.getElementById('nowDate').value
    const nextDate = document.getElementById('nextDate').value

    $('#mask, #loadingImg').show()

    new Promise((resolve) => {
        $.ajax({
            type: 'GET',
            url: '/selfCompareAPIStep3/',
            dataType: 'json',
            data: {
                'nowDate': nowDate,
                'nextDate': nextDate,
            },
            success: function(request) {

                new Promise((resolve2) => {
                    $.ajax({
                        type: 'GET',
                        url: '/selfCompareAPICarMaker/',
                        dataType: 'json',
                        data: {},
                        success: function(request) {
 
                            CreateCarMakerList(request)

                            $('#mask, #loadingImg').hide()
                            $('.step2').children('.section2').hide()
                            $('.step2').children('.section3, .section4').show()
            
                            resolve2()
                        }
                    })
                })
                resolve()
            }
        })
    })
}


function selfCompareAPICarMaker() {

    RemoveChild()
    RemoveTitle(5)

    $('#mask, #loadingImg').show()

    new Promise((resolve) => {
        $.ajax({
            type: 'GET',
            url: '/selfCompareAPICarMaker/',
            dataType: 'json',
            data: {},
            success: function(request) {

                CreateCarMakerList(request)
                $('#mask, #loadingImg').hide()
                resolve()
            }
        })
    })
}

function selfCompareAPICarName(data) {

    let reqData = data

    $('#mask, #loadingImg').show()
    RemoveChild()

    if(reqData) {

        let titleTag = document.getElementById('carMakerTitle')
        titleTag.setAttribute('value', reqData)
        titleTag.setAttribute('name', reqData)
        titleTag.innerHTML = '제조사 : ' + reqData
        
    }
    else {

        RemoveTitle(4)
        reqData = document.getElementById('carMakerTitle').value

    }

    new Promise((resolve) => {
        $.ajax({
            type: 'GET',
            url: '/selfCompareAPICarName/',
            dataType: 'json',
            data: {
                'id': reqData,
            },
            success: function(request) {

                CreateCarNameList(request)
                $('#mask, #loadingImg').hide()
                resolve()
            }
        })
    })    


}

function selfCompareAPICarRegister(register) {
    console.log(data)

    // RemoveChild()

    // $('#mask, #loadingImg').show()

    // new Promise((resolve) => {
    //     $.ajax({
    //         type: 'GET',
    //         url: '/selfCompareAPICarName/',
    //         dataType: 'json',
    //         data: {
    //             'id': data,
    //         },
    //         success: function(request) {

    //             CreateCarRegisterList(request)
    //             $('#mask, #loadingImg').hide()
    //             resolve()
    //         }
    //     })
    // })
}

function selfCompareAPICarSubName(data) {
    console.log(data)

    // RemoveChild()

    // $('#mask, #loadingImg').show()

    // new Promise((resolve) => {
    //     $.ajax({
    //         type: 'GET',
    //         url: '/selfCompareAPICarName/',
    //         dataType: 'json',
    //         data: {
    //             'id': data,
    //         },
    //         success: function(request) {

    //             CreateCarSubNameList(request)
    //             $('#mask, #loadingImg').hide()
    //             resolve()
    //         }
    //     })
    // })
}

function selfCompareAPICarOption(data) {
    console.log(data)

    // RemoveChild()

    // $('#mask, #loadingImg').show()

    // new Promise((resolve) => {
    //     $.ajax({
    //         type: 'GET',
    //         url: '/selfCompareAPICarName/',
    //         dataType: 'json',
    //         data: {
    //             'id': data,
    //         },
    //         success: function(request) {

    //             CreateCarOptionList(request)
    //             $('#mask, #loadingImg').hide()
    //             resolve()
    //         }
    //     })
    // })
}

// 스탭2 UI생성, 삭제

function CreateCarMakerList(data) {
    Object.keys(data).forEach(element => {
        CreateCarMakerTag(document.getElementById('carMaker') , element, data[element])
    })
}
function CreateCarNameList(data) {
    Object.keys(data).forEach(element => {
        CreateCarNameTag(document.getElementById('carName') , element, data[element])
    })
}
function CreateCarRegisterList(data) {
    Object.keys(data).forEach(element => {
        CreateCarRegisterTag(document.getElementById('carRegister') , element, data[element])
    })
}
function CreateCarSubNameList(data) {
    Object.keys(data).forEach(element => {
        CreateCarSubNameTag(document.getElementById('carSubName') , element, data[element])
    })
}
function CreateCarOptionList(data) {
    Object.keys(data).forEach(element => {
        CreateCarOptionTag(document.getElementById('carOption') , element, data[element])
    })
}

function CreateCarMakerTag(element , id, val, func) {

    li = element.appendChild(document.createElement('li'))
    li.setAttribute('onclick', `selfCompareAPICarName('${id}')`)

    div1 = li.appendChild(document.createElement('div'))
    div1.setAttribute('class', 'box')

    div2 = li.appendChild(document.createElement('div'))
    div2.setAttribute('class', 'text1')
    div2.setAttribute('id', id)
    div2.innerHTML = val

}


function CreateCarNameTag(element , id, val, func) {

    li = element.appendChild(document.createElement('li'))
    li.setAttribute('onclick', `selfCompareAPICarRegister('${id}')`)

    div1 = li.appendChild(document.createElement('div'))
    div1.setAttribute('class', 'box')

    div2 = li.appendChild(document.createElement('div'))
    div2.setAttribute('class', 'text1')
    div2.setAttribute('id', id)
    div2.innerHTML = val

}


function CreateCarRegisterTag(element , id, val, func) {

    li = element.appendChild(document.createElement('li'))
    li.setAttribute('onclick', `selfCompareAPICarSubName('${id}')`)

    div1 = li.appendChild(document.createElement('div'))
    div1.setAttribute('class', 'box')

    div2 = li.appendChild(document.createElement('div'))
    div2.setAttribute('class', 'text1')
    div2.setAttribute('id', id)
    div2.innerHTML = val

}


function CreateCarSubNameTag(element , id, val, func) {

    li = element.appendChild(document.createElement('li'))
    li.setAttribute('onclick', `selfCompareAPICarOption('${id}')`)

    div1 = li.appendChild(document.createElement('div'))
    div1.setAttribute('class', 'box')

    div2 = li.appendChild(document.createElement('div'))
    div2.setAttribute('class', 'text1')
    div2.setAttribute('id', id)
    div2.innerHTML = val

}


function CreateCarOptionTag(element , id, val, func) {

    li = element.appendChild(document.createElement('li'))

    div1 = li.appendChild(document.createElement('div'))
    div1.setAttribute('class', 'box')

    div2 = li.appendChild(document.createElement('div'))
    div2.setAttribute('class', 'text1')
    div2.setAttribute('id', id)
    div2.innerHTML = val

}










function RemoveChild() {
    document.getElementById('carMaker').innerHTML = ""
    document.getElementById('carName').innerHTML = ""
    document.getElementById('carRegister').innerHTML = ""
    document.getElementById('carSubName').innerHTML = ""
    document.getElementById('carOption').innerHTML = ""
}

function RemoveTitle(count) {
    textArray = ['세부항목을 선택하세요.', '세부차명을 선택하세요.', '자동차 등록년도를 선택하세요.', '자동차명을 선택하세요.', '제조사를 선택하세요.']
    titleArray = ['carOptionTitle', 'carSubNameTitle', 'carRegisterTitle', 'carNameTitle', 'carMakerTitle']

    for (let i = 0; i < count; i++ ) {
        let titleTag = document.getElementById(titleArray[i])
        titleTag.setAttribute('value', '')
        titleTag.setAttribute('name', '')
        titleTag.innerHTML = textArray[i]
    }
}
