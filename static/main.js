var socket = io.connect('http://' + document.domain + ':' + location.port)
// broadcast a message
socket.on('connect', function () {
    socket.emit('init_conn', {
        data: 'User Connected'
    })

    document.querySelector('#messanger').addEventListener('submit', event => {
        event.preventDefault();
        let user_name = document.querySelector('.username');
        let user_input = document.querySelector('.message');
        console.log(user_name.value, user_input.value);
        if (user_name.value.length > 0 && user_input.value.length > 0) {
            socket.emit('chat_message', {
                user_name: user_name.value,
                message: user_input.value
            })
            // empty the input field
            user_input.value = ''
            user_input.focus();
        } else {
            //add empty string error
        }
    })
})
// capture message
socket.on('my_response', function (msg) {
    console.log(msg)
    if (typeof msg.user_name !== 'undefined') {
        let mm = document.querySelector('#main-message')
        if (mm) {
            mm.remove();
        }
        let newDiv = document.createElement('div');
        newDiv.className = 'msg_bbl';
        newDiv.innerHTML = msg.mess_date +
            ' <b style="color: #000">' + msg.user_name +
            '</b> ' + msg.message;
        document.querySelector('div.message_holder').appendChild(newDiv);
    }
})
socket.on('server_connection', msg => {
    console.log(msg)
})