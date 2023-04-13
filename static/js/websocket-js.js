const getUserId = () => window.location.href.split('/')[4];
const selfMessage = (text) => `<div class="self message"><div class="message-content">${text}</div></div>`;
const message = (text) => `<div class="message"><div class="message-content">${text}</div></div>`;
// const scroll = () => {document.querySelector('#messages').scrollTo(0, document.querySelector('#messages').scrollHeight);};
const messages = document.querySelector('#messages');
const input = document.querySelector('.text-box');
const file = document.querySelector('#file');



function sendImageModal(e, socket) {
    let modal = document.querySelector('.modal');
    let modalImage = document.querySelector('#modal-image');
    let file = e.target.files[0];
    let reader = new FileReader();
    let sendButton = document.querySelector('.send');

    let fileContent;

    modal.style.display = 'flex';

    document.querySelector('.close').addEventListener('click', () => {
        modal.style.display = 'none';
    });

    reader.readAsDataURL(file);

    reader.onload = function (e) {
        modalImage.src = e.target.result;
        fileContent = e.target.result;
    };

    sendButton.addEventListener('click', function () {
        if (socket.readyState === WebSocket.OPEN) {
            data = {
                'type': 'image',
                'content': `${fileContent}`
            };
            socket.send(JSON.stringify(data));
            modal.style.display = 'none';
            messages.innerHTML += selfMessage(`<img src="${fileContent}" alt="socket image" />`);
            // scroll();
        }
    });
}

function socketFun() {
    const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + getUserId() + '/');
    socket.onmessage = function (e) {
        let jsonData = JSON.parse(e.data);
        console.log(jsonData);
        if (jsonData.content.sender != document.querySelector('#user-id').textContent) {
            if (jsonData.type == 'text_message') {
                messages.innerHTML += message(jsonData.content.text);
                // setTimeout(() => {scroll();}, 500);
            } else if (jsonData.type == 'image_message') {
                messages.innerHTML += message(`<img src="${jsonData.content.image}" alt="socket image" />`);
                // setTimeout(() => {scroll();}, 500);
            } else if (jsonData.type == 'member_count_message'){
                console.log(jsonData.content);
            }


        }
    };

    socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
        setTimeout(function () {
            socketFun();
        }, 3000);
    };

    input.onkeyup = function (e) {
        if (e.keyCode === 13) {
            if (socket.readyState === WebSocket.OPEN) {
                messages.innerHTML += selfMessage(input.value);
                socket.send(JSON.stringify({
                    'type': 'text',
                    'content': input.value,
                }));
                input.value = '';
                scroll();
            }
        }
    };

    function checkMember() {
        setTimeout(() => {
            checkMember();

            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    'type': 'get_member_count',
                }));
            }
        }, 2000)
    }

    checkMember();



    file.addEventListener('change', e => {
        sendImageModal(e, socket);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        // scroll();
        socketFun();
    }, 10);
});

