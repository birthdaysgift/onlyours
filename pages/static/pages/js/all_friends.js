$(".all-friends").click(function (event) {
    event.stopPropagation();
});
$(".all-friends-background").click(function (event) {
    $(".all-friends-background").remove();
});

$(".friends-list-icon").click(function(event) {
    clicked = $(event.target);
    if (clicked.hasClass("contact-avatar")) {
        var linkURL = clicked.parent().find(".friend-link").attr("href");
        window.location.href = linkURL;
        return;
    };

    if (clicked.hasClass("friends-list-icon")) {
        var linkURL = clicked.find(".friend-link").attr("href");
        window.location.href = linkURL;
        return;
    };
});
