var socket = io.connect('http://' + document.domain + ':' + location.port)
// broadcast a message
socket.on('connect', function () {
    socket.emit('my event', {
        data: 'User Connected'
    })
    var form = $('form').on('submit', function (e) {
        e.preventDefault()
        let user_name = $('input.username').val()
        let user_input = $('input.message').val()
        console.log(user_name, user_input);

        socket.emit('chat_message', {
            user_name: user_name,
            message: user_input
        })
        // empty the input field
        $('input.message').val('').focus()
    })
})
// capture message
socket.on('my_response', function (msg) {
    console.log(msg)
    if (typeof msg.user_name !== 'undefined') {
        $('h1').remove()
        $('div.message_holder').append('<div class="msg_bbl">' + msg.mess_date +
            ' <b style="color: #000">' + msg.user_name +
            '</b> ' + msg.message + '</div>')
    }
})
socket.on('server_connection', msg => {
    console.log(msg)
})