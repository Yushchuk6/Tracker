const socket = new WebSocket('ws://localhost:8080');

socket.onopen = function (e) {
    console.log('[open] Opened connection');
};

socket.onmessage = function (event) {
    const command = JSON.parse(event.data);

    if (command.type === 'message'){
        console.log(`[message]: ${command.message}`);
    }
    else if (command.type === 'trace'){
        plot.update_trace(command.data);
    }
};