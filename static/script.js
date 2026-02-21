// ===============================
// SIMPLE CHATGPT-STYLE CHAT
// ===============================

async function sendMessage() {

    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // 🔵 Add user message instantly
    const userDiv = document.createElement("div");
    userDiv.classList.add("message", "user");
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    // 🤖 Send to backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // Clear chat and re-render full history
    chatBox.innerHTML = "";

    data.messages.forEach(msg => {
        const div = document.createElement("div");
        div.classList.add("message");
        div.classList.add(msg[0]); // user or assistant
        div.innerText = msg[1];
        chatBox.appendChild(div);
    });

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Press Enter to send
document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
