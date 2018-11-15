$(".friends-text").click( function(event) {
    var url = $(".friends-list-link").attr("href");
    $.get({
        url: url,
        dataType: "html",
        success: function(htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    });
});

$(".form-info-block").keypress(function(event) {
    if ((event.which == 10 && event.ctrlKey) ||
        (event.which == 13 && event.ctrlKey)) {
        event.preventDefault();
        $(".posts-panel > form").submit();
    }
});

$(".add-post").focusin(function(event) {
    $(".form-info-block").animate({
        height: "90px"
    }, {
        duration: 200,
        start: function() {
            $(".form-info-text").css("display", "block");
        }
    });
});

$(".add-post").focusout(function(event) {
    $(".form-info-block").animate({
        height: "65px"
    }, {
        duration: 200,
        complete: function() {
            $(".form-info-text").css("display", "none");
        }
    });
});

$(".close-icon").click(function(event) {
    var url = $(event.target).parent().find(".close-icon-link").attr("href");
    $.get({
        url: url,
        dataType: "html",
        success: function(htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    })
});

$(".photo-text").click(function(event) {
    var url = $(".photos-list-link").attr("href");
    $.get({
        async: true,
        url: url,
        dataType: "html",
        success: function(htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    });
});

$(".photo-avatar").click(function(event) {
    $(".page-detail-photo-background").css("display", "flex");
    var src = $(event.target).attr("src");
    $(".page-photo-img").attr("src", src);
});

$(".page-detail-photo-background").click(function(event) {
    $(".page-detail-photo-background").css("display", "none");
});

$(".video-text").click(function(event) {
    var url = $(".videos-list-link").attr("href");
    $.get({
        async: true,
        url: url,
        dataType: "html",
        success: function(htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    });
});

$(".video-avatar").click(function(event) {
    $(".page-detail-video-background").css("display", "flex");
    var src = $(event.target).attr("src");
    $(".page-video-img").attr("src", src);
});

$(".page-detail-video-background").click(function(event) {
    $(".page-detail-video-background").css("display", "none");
    $(".page-video-img").get(0).pause();
});