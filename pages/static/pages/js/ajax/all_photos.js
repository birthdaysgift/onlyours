$(".all-photos-background").click(function(event) {
    $(".all-photos-background").remove();
});

$(".add-icon").click(function(event) {
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

$(".new-photo-input").change(function(event) {
    $(".new-photo-submit").trigger("click");
});