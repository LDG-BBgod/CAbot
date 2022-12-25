let socket
let connectCheck = false
var rejectMessage


function closeChat() {
    document.getElementById('mask').style.display = 'none'
    document.getElementsByClassName('sectionFix')[0].style.display = 'none'
}


function OpenChat() {
    document.querySelector('#message').focus()
    document.querySelector('#message').onkeyup = (e) => {
        if (e.keyCode === 13) {
            document.querySelector('#sendButton').click()
        }
    }
    document.getElementById('mask').style.display = 'block'
    document.getElementsByClassName('sectionFix')[0].style.display = 'block'
    
    //상담원 연결 안됬을시 소캣연결
    if (!connectCheck) {
        document.getElementsByClassName('chatBoxMiddle')[0].innerHTML = ""
        socket = new WebSocket(`ws://${window.location.host}/ws/${userIP}/`)
    }

    socket.addEventListener('message', (e) => {
        const message = JSON.parse(e.data).message
        const username = JSON.parse(e.data).username
        
        if (username == 'Admin' || username == 'LDJ') {
            if (username == 'LDJ') {
                connectCheck = true
                clearTimeout(rejectMessage)
            }
            $('.chatBoxMiddle').append('<div class="item"><div class="msgContainer"><div class="msg">' + message + '</div></div></div>')
            document.getElementsByClassName('chatBoxMiddle')[0].scrollTop = document.getElementsByClassName('chatBoxMiddle')[0].scrollHeight
        }        
    })
} 


document.getElementById('sendButton').addEventListener('click', () => {

    const message = document.getElementById('message').value

    if (message != '') {

        document.getElementById('message').value = ''

        const textarea = document.getElementById('message')
        textarea.style.height = '40px'
        document.getElementsByClassName('chatBoxMiddle')[0].style.height = '640px'

        $('.chatBoxMiddle').append('<div class="item myItem"><div class="msgContainer myMsgContainer"><div class="msg myMsg">' + message + '</div></div></div>')
        document.getElementsByClassName('chatBoxMiddle')[0].scrollTop = document.getElementsByClassName('chatBoxMiddle')[0].scrollHeight

        if(!connectCheck) {
            // 문자 보내는 api 작성
            socket.send(JSON.stringify({
                'message': message,
                'username': userIP,
                'connectCheck': 'false',
            }))
            rejectMessage = setTimeout(() => {
                socket.send(JSON.stringify({
                    'message': '',
                    'username': userIP,
                    'type': 'reject',
                }))
            }, 60000); //60초간 대기후 상담원 열결 안될시 함수실행
        }
        else {
            socket.send(JSON.stringify({
                'message': message,
                'username': userIP
            }))
        }
    }
})


// textarea 설정
function resize(obj, e) {

    obj.style.height = '0px'
    obj.style.height = obj.scrollHeight + 'px'

    const chatBoxMiddle = document.getElementsByClassName('chatBoxMiddle')[0] 
    chatBoxMiddle.style.height = 680 - obj.scrollHeight + 'px'
    chatBoxMiddle.scrollTop = chatBoxMiddle.scrollHeight

    if (e.keyCode == 13){
        e.returnValue = false
    }

}


//section3 aroowButton
let section3ImgNum = 1

document.getElementsByClassName('arrowLeft')[0].addEventListener('click', () => {
    Section3scroll(-1)
})
document.getElementsByClassName('arrowRight')[0].addEventListener('click', () => {
    Section3scroll(1)
})

function Section3scroll(num){
    const marginMap = {
        '1': '0',
        '2': '-400px',
        '3': '-800px'
    }
    const section = document.getElementById('section3Imgs')
    if(num == 1 && section3ImgNum < 3) {
        section3ImgNum += num
        section.style.marginLeft = marginMap[section3ImgNum]
    }
    else if (num == -1 && section3ImgNum > 1) {
        section3ImgNum += num
        section.style.marginLeft = marginMap[section3ImgNum]
    }
}



//임시
document.getElementsByClassName('alert')[0].addEventListener('click', () => {

    alert('서비스 준비중입니다.')
})
document.getElementsByClassName('alert')[1].addEventListener('click', () => {

    alert('서비스 준비중입니다.')
})
document.getElementsByClassName('alert')[2].addEventListener('click', () => {

    alert('서비스 준비중입니다.')
})