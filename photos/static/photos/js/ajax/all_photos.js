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
    $(event.target).parent().addClass('selected');
    var url = $(event.target.previousElementSibling).attr('href');
    $.get({
        url: url,
        success: function(htmlData) {
            $('.all-photos-background').prepend(htmlData);
        }
    });
});

$(document).keypress(function(event) {
    var left_key = KeyEvent.DOM_VK_LEFT;
    var right_key = KeyEvent.DOM_VK_RIGHT;
    if ((event.keyCode === left_key) || (event.keyCode === right_key)) {
        var selected_photo = $('.photo-avatar-wrapper.selected');
        var opened_photo = $('.detail-photo-background');
        if ((selected_photo.length === 1) && (opened_photo.length === 1)){
            opened_photo.remove();
            selected_photo.removeClass('selected');
            if (event.keyCode === right_key) {
                var next_photo = selected_photo.next();
            }
            if (event.keyCode === left_key) {
                var next_photo = selected_photo.prev();
            }
            var url = next_photo.find('.detail-photo-link').attr('href');
            $.get({
                url: url,
                success: function(htmlData) {
                    next_photo.addClass('selected');
                    $('.all-photos-background').prepend(htmlData);
                }
            });
            next_photo.addClass('selected');
        }
    }
});

$(".new-photo-input").change(function(event) {
    $(".new-photo-submit").trigger("click");
});