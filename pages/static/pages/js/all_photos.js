$(".all-photos-background").click(function(event) {
    $(".all-photos-background").remove();
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
    var url = $(event.target.previousElementSibling).attr('href');
    $.get({
        url: url,
        success: function(htmlData) {
            $('.all-photos-background').prepend(htmlData);
        }
    });
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