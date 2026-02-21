let currentConversationId = null;

async function createNewChat() {
    const response = await fetch("/new_chat", { method: "POST" });
    const data = await response.json();

    currentConversationId = data.conversation_id;
    document.getElementById("chatBox").innerHTML = "";
    loadConversations();
}

async function loadConversations() {
    const response = await fetch("/get_conversations");
    const conversations = await response.json();

    const list = document.getElementById("conversationList");
    list.innerHTML = "";

    conversations.forEach(conv => {
        list.innerHTML += `
            <div class="conversation-item"
                 onclick="loadMessages(${conv[0]})">
                 ${conv[1]}
            </div>
        `;
    });
}

async function loadMessages(conversationId) {
    currentConversationId = conversationId;

    const response = await fetch(`/get_messages/${conversationId}`);
    const messages = await response.json();

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = "";

    messages.forEach(msg => {
        if (msg[0] === "user") {
            chatBox.innerHTML += `<div class="user-msg"><p>${msg[1]}</p></div>`;
        } else {
            chatBox.innerHTML += `<div class="ai-msg"><p>${msg[1]}</p></div>`;
        }
    });
}

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const chatBox = document.getElementById("chatBox");
    const userMessage = input.value.trim();
    if (!userMessage) return;

    if (!currentConversationId) {
        await createNewChat();
    }

    chatBox.innerHTML += `<div class="user-msg"><p>${userMessage}</p></div>`;
    input.value = "";

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            message: userMessage,
            conversation_id: currentConversationId
        })
    });

    const data = await response.json();

    chatBox.innerHTML += `<div class="ai-msg"><p>${data.response}</p></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

window.onload = loadConversations;
