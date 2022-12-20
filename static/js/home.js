let socket
let connectCheck = false
var rejectMessage


function closeChat() {
    document.getElementById('mask').style.display = 'none'
    document.getElementsByClassName('sectionFix')[0].style.display = 'none'
}


function OpenChat() {
    document.getElementById('mask').style.display = 'block'
    document.getElementsByClassName('sectionFix')[0].style.display = 'block'
    
    //상담원 연결 안됬을시 소캣연결
    if (!connectCheck) {
        document.getElementsByClassName('chatBoxMiddle')[0].innerHTML = ""
        console.log(`ws://${window.location.host}/ws/${userIP}`)
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
        }        
    })
} 


document.getElementById('sendButton').addEventListener('click', () => {

    const message = document.getElementById('message').value

    document.getElementById('message').value = ''
    $('.chatBoxMiddle').append('<div class="item myItem"><div class="msgContainer myMsgContainer"><div class="msg myMsg">' + message + '</div></div></div>')


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
})


