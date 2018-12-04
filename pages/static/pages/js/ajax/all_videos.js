$(".all-videos-background").click(function(event) {
    $(".all-videos-background").remove();
});

$('.video-list-window').click(function(event) {
    event.stopPropagation();
})

$('.add-icon').click(function(event) {
    if ($('.youtube-icon').css('display') === 'none') {
        $('.youtube-icon').animate({
            right: '30px',
        }, {
            duration: 200,
            start: function(event) {
                $('.youtube-icon').css('display', 'inline-block');
            }
        })
        $('.upload-icon').animate({
            right: '70px',
        }, {
            duration: 200,
            start: function(event) {
                $('.upload-icon').css('display', 'inline-block');
            }
        })
    } else {
        $('.youtube-icon').animate({
            right: '0px',
        }, {
            duration: 200,
            complete: function(event) {
                $('.youtube-icon').css('display', 'none');
            }
        })
        $('.upload-icon').animate({
            right: '0px',
        }, {
            duration: 200,
            complete: function(event) {
                $('.upload-icon').css('display', 'none');
            }
        })
    }
})

$(".upload-icon").click(function(event) {

    $(".new-video-input").click(function(event){
        event.stopPropagation();
    });
    event.stopPropagation();
    $(".new-video-input").trigger("click");
});

$(".new-video-submit").click(function(event) {
    event.stopPropagation();
});

$(".video-list-avatar").click(function(event){
    event.stopPropagation();
    var url = $(event.target.previousElementSibling).attr('href');
    $.get({
        url: url,
        success: function(htmlData) {
            $('.all-videos-background').prepend(htmlData);
        }
    });
});

$(".delete-video-icon").click(function(event){
    event.stopPropagation();
    var url = $(event.target).find(".delete-video-link").attr("href");
    $.get({
        async: true,
        url: url,
        success: function(event) {
            window.location.reload(true);
        }
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
});

$(".new-video-input").change(function(event) {
    $(".new-video-submit").trigger("click");
});