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

$(".photo-avatar-wrapper").click(function(event) {
    var url = $(event.target.previousElementSibling).attr('href');
    $.get({
        url:url,
        dataType: 'html',
        success: function(htmlData) {
            $('.wrapper').prepend(htmlData);
            $(event.currentTarget).addClass('selected');
        }
    })
});

$(document).keypress(function(event) {
    if ($('.all-photos-background').length === 0) {

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
                        $('.wrapper').prepend(htmlData);
                    }
                });
                next_photo.addClass('selected');
            }
        }
    }
});

