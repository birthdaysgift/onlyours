$(".all-videos-background").click(function(event) {
    $(".all-videos-background").remove();
});

$(".add-new-video").click(function(event) {
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