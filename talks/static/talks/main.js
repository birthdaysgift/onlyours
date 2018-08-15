function lastMessageIntoView() {
    selectedPageNum = document.body.querySelector(
        ".pages-list > .selected"
    ).textContent;
    if (parseInt(selectedPageNum, 10) === 1) {
        messages = document.body.querySelectorAll("#messages > p");
        lastMessage = messages[messages.length-1];
        lastMessage.scrollIntoView();
    }
}

function currentContactIntoView() {
    currentContact = document.body.querySelector("#contacts > p > span");
    currentContact.scrollIntoView();
}

document.addEventListener("DOMContentLoaded", lastMessageIntoView);
document.addEventListener("DOMContentLoaded", currentContactIntoView);