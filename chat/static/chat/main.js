function lastMessageIntoView() {
    messages = document.body.querySelectorAll("#chat > p");
    lastMessage = messages[messages.length-1];
    lastMessage.scrollIntoView();
}

document.addEventListener("DOMContentLoaded", lastMessageIntoView);