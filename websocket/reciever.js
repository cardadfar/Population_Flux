let socket = new WebSocket("ws://localhost:8765");

socket.onmessage = function(event) {
    var dataRaw = event.data;
    var net = 0;
    for(var i = 0; i < dataRaw.length; i++) {
        if(dataRaw[i] == 0) {net += 1;}
        else if(dataRaw[i] == 1)  {net -= 1;}
    }
    console.log(net);
};

