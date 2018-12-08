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
    var url = $(event.target.previousElementSibling).attr('href');
    console.log(url);
    $.get({
        url:url,
        dataType: 'html',
        success: function(htmlData) {
            $('.wrapper').prepend(htmlData);
        }
    });
});

$(".video-avatar").click(function(event) {
    var url = $(event.target.previousElementSibling).attr('href');
    $.get({
        url:url,
        dataType: 'html',
        success: function(htmlData) {
            $('.wrapper').prepend(htmlData);
        }
    });
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


