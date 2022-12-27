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

var nexDay = new Date(today.setFullYear(today.getFullYear() + 1))
var nextYear = nexDay.getFullYear();
var nextMonth = ('0' + (nexDay.getMonth() + 1)).slice(-2)
var nextDay = ('0' + nexDay.getDate()).slice(-2)
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
    nowDate = document.getElementById('nowDate').value
    nextDate = document.getElementById('nextDate').value

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
                $('#mask, #loadingImg').hide()
                $('.step2').children('.section2').hide()
                $('.step2').children('.section3, .section4').show()

                resolve()
            }
        })
    })
}
