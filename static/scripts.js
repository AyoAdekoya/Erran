function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    if (userInput.value.trim() === "") {
        return;
    }

    // Append user's message to chat box
    const userMessage = document.createElement('p');
    userMessage.textContent = "You: " + userInput.value;
    chatBox.appendChild(userMessage);

    // Send message to Flask server
    fetch('/get', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'msg=' + encodeURIComponent(userInput.value),
    })
    .then(response => response.text())
    .then(data => {
        // Append chatbot's response to chat box
        const botMessage = document.createElement('p');
        botMessage.textContent = "Chatbot: " + data;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    // Clear input field
    userInput.value = "";
}