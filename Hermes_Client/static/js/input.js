var isActive = false;

function microphone_toggle() {
    const microphoneIcon = document.getElementById("clickable");
    const microphoneCircle = document.getElementById("microphoneCircle");
    const microphoneInner = document.getElementById("microphoneInner");

    if (isActive) {
        microphoneIcon.classList.remove('active');
        microphoneCircle.style.borderColor = "#0099CC";
        microphoneInner.style.backgroundColor = "rgba(128, 128, 128, 0.5)";
        isActive = false;
        recognition.stop();
    } else {
        microphoneIcon.classList.add('active');
        microphoneCircle.style.borderColor = "red";
        microphoneInner.style.backgroundColor = "rgba(255, 182, 193, 0.5)";
        isActive = true;
        recognition.start();
    }
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const contentDiv = document.getElementById("text");

    if (userInput) {
        contentDiv.innerHTML += `<p>Sent: ${userInput}</p>`;
        socket.emit('send_message', { text: userInput, device: 'your_device_name' });
        document.getElementById("userInput").value = "";
    } else {
        contentDiv.innerHTML += `<p style="color: red;">Please enter a sentence.</p>`;
    }
}

// Listen for message_response from the server - Moved outside sendMessage
socket.on('message_response', function (data) {
    const contentDiv = document.getElementById("text");

    if (data.status === 'success') {
        contentDiv.innerHTML += `<p>Response received: ${data.output}</p>`;
    } else {
        contentDiv.innerHTML += `<p style="color: red;">Error: ${data.message}</p>`;
    }
});

var restart = true;
var on = false;
var lastFinal = "";
var content = document.querySelector(".demo");
var speechRecognition = window.speechRecognition || window.webkitSpeechRecognition;
var recognition = new speechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

recognition.onstart = function () {
    console.log("voice is activated");
};

recognition.onend = function () {
    console.log("voice is no longer activated");
    if (on) { toggle(false); }
};

recognition.onresult = function (event) {
    const current = event.resultIndex;
    const transcript = event.results[current][0].transcript;
    const contentDiv = document.getElementById("text");

    if (event.results[current].isFinal) {
        if (transcript !== lastFinal) {
            lastFinal = transcript;
            socket.emit('send_message', { text: transcript, device: 'your_device_name' });
            contentDiv.innerHTML += `<p>Heard: ${transcript}</p>`;
        }
    }
};

recognition.onerror = function (event) {
    console.log('Speech recognition error detected: ' + event.error);
    recognition.stop();
};

function removeThis() { event.target.remove(); }
function editThis(editable) { event.target.setAttribute("contenteditable", editable); }
