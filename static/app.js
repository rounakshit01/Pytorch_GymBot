document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");

    // Function to send the message
    async function sendMessage() {
        const userMessage = userInput.value.trim();
        
        if (userMessage === "") return; // Do nothing if input is empty

        // Append user's message to the chatbox
        appendMessage("User: " + userMessage, "user-message");

        // Clear the input field
        userInput.value = "";

        // Send the message to the Flask server
        try {
            const response = await fetch("http://127.0.0.1:5000/chat", { // Use full URL here
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();
            const botMessage = data.reply || "I'm sorry, I didn't understand that.";

            // Append chatbot's response to the chatbox
            appendMessage("GymBot: " + botMessage, "bot-message");

        } catch (error) {
            console.error("Error:", error);
            appendMessage("GymBot: Sorry, there was an error connecting to the server.", "bot-message");
        }
    }

    // Function to append messages to the chatbox
    function appendMessage(message, className) {
        const messageElement = document.createElement("p");
        messageElement.textContent = message;
        messageElement.className = className;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the bottom
    }

    // Attach sendMessage to the Send button and Enter key
    document.querySelector("button").addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessage();
    });
});



