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
        case 'trakers':
            map.update_trackers(data);
            console.log(`[update] trakers updated`);
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

function set_list_attributes(html_el, attr) {
    for (const [key, value] of Object.entries(attr)) {
        html_el.setAttribute(key, value);
    }
}