let socket = new WebSocket(`ws://${window.location.host}/ws/${userIP}/`)


setTimeout(() => {
    socket.send(JSON.stringify({
        'message': '상담원이 연결되었습니다.',
        'username': 'LDJ'
    }))
}, 500);


socket.addEventListener('message', (e) => {
    const message = JSON.parse(e.data).message
    const username = JSON.parse(e.data).username
    console.log(username)
    if (username != 'Admin' && username != 'LDJ') {
        $('.chatBoxMiddle').append('<div class="item"><div class="msgContainer"><div class="msg">' + message + '</div></div></div>')
    }
})


document.getElementById('sendButton').addEventListener('click', () => {
    const message = document.getElementById('message').value
    document.getElementById('message').value = ''
    $('.chatBoxMiddle').append('<div class="item myItem"><div class="msgContainer myMsgContainer"><div class="msg myMsg">' + message + '</div></div></div>')

    socket.send(JSON.stringify({
        'message': message,
        'username': 'LDJ'
    }))
})
