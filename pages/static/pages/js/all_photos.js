$(".wrapper > .all-photos-background").click(function(event) {
    $(".all-photos-background").remove();
});

$(".all-photos-detail-photo-background").click(function(event){
    event.stopPropagation();
    $(".all-photos-detail-photo-background").css("display", "none");
});

$(".add-new-photo").click(function(event) {
    $(".new-photo-input").click(function(event){
        event.stopPropagation();
    });
    event.stopPropagation();
    $(".new-photo-input").trigger("click");
});

$(".new-photo-submit").click(function(event) {
    event.stopPropagation();
});

$(".photo-list-avatar").click(function(event){
    event.stopPropagation();
    var src = $(event.target).attr("src");
    $(".all-photos-photo-img").attr("src", src);
    $(".all-photos-detail-photo-background").css("display", "flex");
});

$(".delete-photo-icon").click(function(event){
    event.stopPropagation();
    var url = $(event.target).find(".delete-photo-link").attr("href");
    $.get({
        async: true,
        url: url,
        success: function(event) {
            window.location.reload(true);
        }
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
});

$(".new-photo-input").change(function(event) {
    $(".new-photo-submit").trigger("click");
});