const socket = new WebSocket('ws://localhost:8080');

socket.onopen = function (e) {
    console.log('[open] Opened connection');
};

socket.onmessage = function (event) {
    const command = JSON.parse(event.data);
    const data = command.data
    console.log(data)
    switch (command.type){
        case 'message':
            console.log(`[message]: ${data}`);
            break;
        case 'trace':
            plot.update_trace(data);
            break;
        case 'layout':
            plot.update_layout(data);
            break;
        case 'slider':
            const slider = document.getElementById('slider');
            set_list_attributes(slider, data)
            break;
        case 'test':
            console.log(`[test] test data: ${data}`);
            break;
    }
};

function send_socket(message){
    socket.send(message)
}

function set_list_attributes(html_el, attr){
    for (const [key, value] of Object.entries(attr)) {
        html_el.setAttribute(key, value);
    }
}