$(".wrapper > .all-videos-background").click(function(event) {
    $(".all-videos-background").remove();
});

$(".all-videos-detail-video-background").click(function(event){
    event.stopPropagation();
    $(".all-videos-detail-video-background").css("display", "none");
    $(".all-videos-video-img").get(0).pause();
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
    var src = $(event.target).attr("video");
    $(".all-videos-video-img").attr("src", src);
    $(".all-videos-detail-video-background").css("display", "flex");
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