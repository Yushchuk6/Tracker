const socket = new WebSocket('ws://localhost:8080');

socket.onopen = function (e) {
    console.log('[open] connection opened');
};

socket.onclose = function (e) {
    console.log('[close] connection closed');
};

socket.onmessage = function (event) {
    const command = JSON.parse(event.data);
    const data = command.data

    switch (command.type) {
        case 'message':
            console.log(`[message]: ${data}`);
            break;
        case 'path':
            map.update_path(data);
            console.log(`[update] path updated`);
            break;
        case 'trackers':
            map.update_trackers(data);
            console.log(`[update] trackers updated`);
            break;
        case 'target':
            map.update_target(data);
            console.log(`[update] target updated`);
            break;
        case 'target_guess':
            map.update_target_guess(data);
            console.log(`[update] target guess updated`);
            break;
        case 'test':
            console.log(`[test] test data: ${data}`);
            break;
    }
};

function send_socket(message) {
    socket.send(message)
}
