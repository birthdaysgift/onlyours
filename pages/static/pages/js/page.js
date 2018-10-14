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