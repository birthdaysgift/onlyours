$(".contact-icon").click(function(event) {
    clicked = $(event.target);
    if (clicked.hasClass("last-message-text")) {
        var linkURL = clicked.parent().find(".talk-link").attr("href");
        window.location.href = linkURL;
        return;
    };

    if (clicked.hasClass("contact-icon")) {
        var linkURL = clicked.find(".talk-link").attr("href");
        window.location.href = linkURL;
        return;
    };
});


$(".contact-username, .contact-avatar").click(function(event) {
    clicked = $(event.target);
    var linkURL = clicked.parent().find(".contact-link").attr("href");
    window.location.href = linkURL;
});