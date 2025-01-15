async function sendMessage(to, message, csrf_token) {
    addSentMessage(message, new Date());
    
    const response = await fetch('/api/v1/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ to, message })
    });

    if (!response.ok) {
        throw new Error('Failed to send message');
    }

    await response.json();
}

async function getMessageHistory(from) {
    const response = await fetch(`/api/v1/get-messages?user=${from.username}`);
    if (!response.ok) {
        throw new Error('Failed to get message history');
    }
    const data = await response.json();
    const loading = document.querySelector('#loading-messages');
    for(let i = 0; i < data.length; i++){
        const message = data[i];
        if (message.type === 'sent') {
            addSentMessage(message.content, new Date(message.timestamp * 1000));
        } else {
            addReceivedMessage(message.content, from, new Date(message.timestamp * 1000), true);
        }
    }
    loading.classList.add('hidden');
    scrollChatAreaToBottom();
}

function scrollChatAreaToBottom() {
    const container = document.querySelector('#messages-container');
    container.scrollTop = container.scrollHeight;
}

function ensureDateElementExists(day = new Date()) {
    const messagesContainer = document.querySelector('#messages-container');
    const dateString = day.toISOString().split('T')[0];
    const dateDisplayString = day.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    const dateElement = document.getElementById(dateString);
    if (!dateElement) {
        const dateElement = document.createElement('p');
        dateElement.id = dateString;
        dateElement.innerText = dateDisplayString;
        dateElement.classList.add('date-container');
        messagesContainer.appendChild(dateElement);
    }
}

function addSentMessage(message, when=new Date()) {
    const messagesContainer = document.querySelector('#messages-container');
    ensureDateElementExists();
    const messageElement = document.createElement('div');
    messageElement.classList.add('sent-message');
    // get time string from when in the format hh:mm ensure both are two digits
    const timeString = when.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const getMessageLine = (text) => `<span>${text}</span>`;
    const htmlTemplate = `
        <div class="text-wrap rounded-lg shadow-md p-2 bg-blue-200/30 text-sm">
            <div class="flex flex-col gap-1">
                <span class="max-w-[450px] text-wrap break-words flex flex-col">${message.split('\n').map(getMessageLine).join('')}</span>
                <span class="text-xs text-gray-400 self-end font-medium">${timeString}</span>
            </div>
        </div>
    `;
    messageElement.innerHTML = htmlTemplate;
    messagesContainer.appendChild(messageElement);
    return messageElement;
}

function addReceivedMessage(message, user, when, isCurrentReceiver) {
    const messagesContainer = document.querySelector('#messages-container');
    ensureDateElementExists();
    const messageElement = document.createElement('div');
    messageElement.classList.add('received-message');
    const timeString = when.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    const getMessageLine = (text) => `<span>${text}</span>`;
    const htmlTemplate = `
        <img class="w-[20px]" src="https://api.dicebear.com/9.x/initials/svg?seed=${user.first_name}&size=20&radius=50" alt="${user.first_name} Avatar" />
        <div class="max-w-sm rounded-lg shadow-md p-2 bg-gray-200/30 text-sm">
            <div class="flex flex-col gap-1">
                <span class="max-w-[450px] text-wrap break-words flex flex-col">${message.split('\n').map(getMessageLine).join('')}</span>
                <span class="text-xs text-gray-400 self-end font-medium">${timeString}</span>
            </div>
        </div>
    `;
    messageElement.innerHTML = htmlTemplate;

    if(isCurrentReceiver){
        messagesContainer.appendChild(messageElement);  
    }else{
        const usersContainer = document.querySelector('#users-container');
        const msgIndicator = usersContainer.querySelector(`#user-${user.username} .new-message-indicator`);
        document.querySelector(`#user-${user.username}`).classList.add('unread-message');
        msgIndicator.classList.remove('hidden');
    } 
}