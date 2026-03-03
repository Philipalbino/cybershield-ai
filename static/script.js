// ===============================
// CHATGPT-STYLE CHAT (Improved)
// ===============================

async function sendMessage() {

    const input = document.getElementById("message");
    const message = input.value.trim();
    const chatBox = document.getElementById("chat-box");

    if (!message) return;

    // =========================
    // Add USER message
    // =========================
    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");

    const userContent = document.createElement("div");
    userContent.classList.add("message-content");
    userContent.innerText = message;

    userMessage.appendChild(userContent);
    chatBox.appendChild(userMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    // =========================
    // Add Typing Indicator
    // =========================
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "assistant");

    const typingContent = document.createElement("div");
    typingContent.classList.add("message-content");
    typingContent.innerText = "CyberShield AI is typing...";

    typingDiv.appendChild(typingContent);
    chatBox.appendChild(typingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove typing indicator
        chatBox.removeChild(typingDiv);

        // =========================
        // Add Assistant Message
        // =========================
        const botMessage = document.createElement("div");
        botMessage.classList.add("message", "assistant");

        const botContent = document.createElement("div");
        botContent.classList.add("message-content");

        botMessage.appendChild(botContent);
        chatBox.appendChild(botMessage);

        // Streaming effect (typing animation)
        let text = data.reply;
        let i = 0;

        function typeWriter() {
            if (i < text.length) {
                botContent.innerText += text.charAt(i);
                i++;
                chatBox.scrollTop = chatBox.scrollHeight;
                setTimeout(typeWriter, 10); // speed of typing
            }
        }

        typeWriter();

    } catch (error) {

        typingContent.innerText = "Error connecting to server.";

    }
}

// ===============================
// Press Enter to Send
// ===============================
document.getElementById("message").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
