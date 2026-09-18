// ==========================================
// CSRF COOKIE
// ==========================================
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie) {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function friendrequest(receiveId,buttonElement){
    
    console.log("Sending request to:", receiveId);
    console.log("Clicked button:", buttonElement);

    fetch(`/messenger/sendrequest/${receiveId}/`,{
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => {
        console.log("HTTP status:", response.status);
        return response.json()
    })
    .then(data=>{
        console.log("Server response:", data);
        if (data.status === "PENDING") {
            buttonElement.innerText = "Requested";
            buttonElement.disabled = true;
        }
        else if (data.status === "ACCEPTED") {
            buttonElement.innerText = "Friends";
            buttonElement.disabled = true;
        }
        else if (data.status === "REJECTED") {
            buttonElement.innerText = "Requested";
            buttonElement.disabled = true;
        }
        else {
            console.log("Unexpected status:", data.status);
        }
    })
    .catch(error =>{
        console.error("Friend request error:",error);
    });
}

function openNotificationModal(){
    let modal=document.getElementById("notificationModal");
    if(modal){
        modal.style.display="flex";
    }
}

function closeNotificationModal(){
    let modal=document.getElementById("notificationModal");
    if(modal){
        modal.style.display="none";
    }
}

window.addEventListener("click",function(event){
    let modal=document.getElementById("notificationModal");
    if(modal && event.target === modal){
        modal.style.display="none";
    }
});

function acceptRequest(notificationId,buttonElement){
    fetch(`/messenger/sendresponse/accept/${notificationId}/`,{
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        } 
    })
    .then(response=>response.json())
    .then(data =>{
        if(data.status === "ACCEPTED"){
            let card=document.getElementById(`notification-${notificationId}`);
            if(card){
                card.remove();
            }
        }
    })
    .catch(error => {
        console.error("Accept request error:",error);
    });
}

function rejectRequest(notificationId, button){
    fetch(`/messenger/sendresponse/reject/${notificationId}/`,{
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        } 
    })
    .then(response => response.json())
    .then(data => {
        if(data.status=="REJECTED"){
            let card=document.getElementById(`notification-${notificationId}`);
            if(card){
                card.remove();
            }
        }
    })
    .catch(error => {
        console.error("Reject request error:",error);
    });
}

// ==========================================
// LOAD MESSAGES
// ==========================================
function loadMessages() {
    fetch(`/messenger/chat/${friendId}/messages/`)
    .then(response => response.json())
    .then(data => {
        if (data.status !== "success") {
            return;
        }

        let messageList =document.getElementById("messageList");
        messageList.innerHTML = "";

        data.messages.forEach(message => {
            let messageDiv =document.createElement("div");

            if (message.sender_id === currentUserId) {
                messageDiv.className = "message my_message";
            }
            else {
                messageDiv.className = "message friend_message";
            }
            messageDiv.innerHTML = `<div class="message_text">
                                        ${escapeHtml(message.message)}
                                    </div>
                                    <small class="message_time">${message.created_at}</small>`;
            messageList.appendChild(messageDiv);
        });

        // Scroll to bottom
        messageList.scrollTop =messageList.scrollHeight;
    })
    .catch(error => {
        console.error("Loading messages error:",error);
    });
}

// ==========================================
// SEND MESSAGE
// ==========================================
function sendMessage() {
    let input =document.getElementById("messageInput");
    let message =input.value.trim();

    if (message === "") {
        return;
    }

    let formData = new FormData();

    formData.append("message",message);
    fetch(`/messenger/chat/${friendId}/send/`,{
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        }
    )
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === "success") {
            input.value = "";
            loadMessages();
        }
    })
    .catch(error => {
        console.error("Send message error:",error);
    });
}

// ==========================================
// ENTER KEY
// ==========================================
document.addEventListener("DOMContentLoaded",function() {
        let input =document.getElementById("messageInput");

        if (input) {
            input.addEventListener("keydown",function(event) {
                    if (event.key === "Enter") {
                        event.preventDefault();
                        sendMessage();
                    }
                }
            );
        }
        loadMessages();
        // Refresh messages every 2 seconds
        setInterval(loadMessages,2000);
    }
);

// ==========================================
// ESCAPE HTML
// ==========================================
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}