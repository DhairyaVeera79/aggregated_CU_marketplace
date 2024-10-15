/* static/js/scripts.js */

document.addEventListener('DOMContentLoaded', function () {
    // Chatbot Button and Window Functionality
    const chatbotButton = document.getElementById('chatbot-button');
    const chatbotWindow = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('close-btn');
    const maximizeBtn = document.getElementById('maximize-btn');
    const chatbotSendBtn = document.getElementById('chatbot-send-btn');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotChat = document.getElementById('chatbot-chat');

    // Toggle Chatbot Window Visibility
    chatbotButton.addEventListener('click', function () {
        chatbotWindow.classList.toggle('d-none');
        // Remove maximized class when opening the window
        if (!chatbotWindow.classList.contains('d-none')) {
            chatbotWindow.classList.remove('maximized');
        }
    });

    // Close Chatbot Window
    closeBtn.addEventListener('click', function () {
        chatbotWindow.classList.add('d-none');
    });

    // Maximize/Restore Chatbot Window
    maximizeBtn.addEventListener('click', function () {
        chatbotWindow.classList.toggle('maximized');
        // Adjust the chat area when maximizing/restoring
        if (chatbotWindow.classList.contains('maximized')) {
            // Optional: Perform any additional actions when maximized
        } else {
            // Optional: Perform any additional actions when restored
        }
        // Scroll to bottom after maximizing/restoring
        setTimeout(() => {
            chatbotChat.scrollTop = chatbotChat.scrollHeight;
        }, 300); // Match transition duration
    });

    // Chatbot Send Button Functionality
    chatbotSendBtn.addEventListener('click', function () {
        const message = chatbotInput.value.trim();
        if (message !== '') {
            // Display user message
            const userMsg = document.createElement('div');
            userMsg.classList.add('user-message');
            userMsg.innerHTML = `<strong>You:</strong> ${message}`;
            chatbotChat.appendChild(userMsg);

            // Clear input
            chatbotInput.value = '';

            // Placeholder for bot response
            const botMsg = document.createElement('div');
            botMsg.classList.add('bot-response');
            botMsg.innerHTML = `<strong>Bot:</strong> This is a placeholder response.`;
            chatbotChat.appendChild(botMsg);

            // Scroll to bottom
            chatbotChat.scrollTop = chatbotChat.scrollHeight;
        }
    });

    // Allow pressing 'Enter' to send message in Chatbot Window
    chatbotInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            chatbotSendBtn.click();
        }
    });

    // Copy Email Functionality
    const copyEmailBtn = document.getElementById('copy-email-btn');
    if (copyEmailBtn) {
        copyEmailBtn.addEventListener('click', function () {
            const emailSpan = document.getElementById('seller-email');
            const email = emailSpan.textContent;

            // Use the Clipboard API if available
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(email).then(function () {
                    alert('Email address copied to clipboard!');
                }, function () {
                    alert('Failed to copy email address.');
                });
            } else {
                // Fallback to older method using a temporary textarea
                const tempTextarea = document.createElement('textarea');
                tempTextarea.value = email;
                // Avoid scrolling to bottom
                tempTextarea.style.position = 'absolute';
                tempTextarea.style.left = '-9999px';
                document.body.appendChild(tempTextarea);
                tempTextarea.focus();
                tempTextarea.select();

                try {
                    const successful = document.execCommand('copy');
                    if (successful) {
                        alert('Email address copied to clipboard!');
                    } else {
                        alert('Failed to copy email address.');
                    }
                } catch (err) {
                    alert('Failed to copy email address.');
                }

                document.body.removeChild(tempTextarea);
            }
        });
    }
});
