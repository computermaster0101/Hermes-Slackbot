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
    if (userInput) {
        alert("Message sent: " + userInput);
        document.getElementById("userInput").value = "";
    } else {
        alert("Please enter a sentence.");
    }
}

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
    content.textContent = transcript;
    if (event.results[current].isFinal) {
        if (transcript !== lastFinal) {
            lastFinal = transcript;
            addThis = document.createElement('p');
            addThis.textContent = transcript;
            addThis.setAttribute("oncontextmenu", "removeThis();return false;");
            addThis.setAttribute("onclick", "editThis(true)");
            addThis.setAttribute("onfocusout", "editThis(false)");
            contentDiv.appendChild(addThis);
            content.textContent = "";
        }
    }
};
recognition.onerror = function (event) {
    console.log('Speech recognition error detected: ' + event.error);
    recognition.stop();
};

function toggle(clicked) {
    element = document.getElementById("clickable");
    contentDiv = document.getElementById("contentText");
    if (on) {
        on = false;
        element.setAttribute("style", "color: #0099CC");
        recognition.stop();
        if ((restart) && (clicked == false)) { toggle(false); }
    } else {
        on = true;
        element.setAttribute("style", "color: red");
        recognition.start();
    }
}

function removeThis() { event.target.remove(); }
function editThis(editable) { event.target.setAttribute("contenteditable", editable); }
