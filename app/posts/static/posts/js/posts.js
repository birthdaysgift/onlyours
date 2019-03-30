function setLike(elem) {
    var likeIcon = $(elem).find('.like-icon');
    if (!likeIcon.hasClass('like-selected')) {
        likeIcon.addClass('like-selected');
        var likeValue = $(elem).find('.like-value');
        var value = parseInt(likeValue.text());
        if (isNaN(value))
            value = 0;
        value++;
        if (value === 0)
            value = '';
        likeValue.text(value);
    }
}

function clearLike(elem) {
    var likeIcon = $(elem).find('.like-icon');
    if (likeIcon.hasClass('like-selected')) {
        likeIcon.removeClass('like-selected');
        var likeValue = $(elem).find('.like-value');
        var value = parseInt(likeValue.text());
        if (isNaN(value))
            value = 0;
        value--;
        if (value === 0)
            value = '';
        likeValue.text(value);
    }
}

function setDislike(elem) {
    var dislikeIcon = $(elem).find('.dislike-icon');
    if (!dislikeIcon.hasClass('dislike-selected')) {
        dislikeIcon.addClass('dislike-selected');
        var dislikeValue = $(elem).find('.dislike-value');
        var value = parseInt(dislikeValue.text());
        if (isNaN(value))
            value = 0;
        value++;
        if (value === 0)
            value = '';
        dislikeValue.text(value);
    }
}

function clearDislike(elem) {
    var dislikeIcon = $(elem).find('.dislike-icon');
    if (dislikeIcon.hasClass('dislike-selected')) {
        dislikeIcon.removeClass('dislike-selected');
        var dislikeValue = $(elem).find('.dislike-value');
        var value = parseInt(dislikeValue.text());
        if (isNaN(value))
            value = 0;
        value--;
        if (value === 0)
            value = '';
        dislikeValue.text(value);
    }
}

function initialize_events() {
    $('.like').click(function(event) {
        var url = $(event.currentTarget).find('.like-link').attr('href');
        $.get({
            url: url
        });
        var likeIcon = $(event.currentTarget).find('.like-icon');
        var dislike = $(event.currentTarget).siblings('.dislike');
        if (likeIcon.hasClass('like-selected')) {
            clearLike(event.currentTarget);
        } else {
            setLike(event.currentTarget);
            clearDislike(dislike);
        }
    });

    $('.dislike').click(function(event) {
        var url = $(event.currentTarget).find('.dislike-link').attr('href');
        $.get({
            url: url
        });
        var dislikeIcon = $(event.currentTarget).find('.dislike-icon');
        var like = $(event.currentTarget).siblings('.like');
        if (dislikeIcon.hasClass('dislike-selected')) {
            clearDislike(event.currentTarget);
        } else {
            setDislike(event.currentTarget);
            clearLike(like);
        }
    })

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
            async: true,
            url: url,
            dataType: "html",
            success: function(htmlData) {
                $(".wrapper").prepend(htmlData);
            }
        })
    });

    $('.more-posts-btn').click(function(event) {
        var url = $(event.target).parent().find('.more-posts-link').attr('href');
        $.get({
            url: url,
            dataType: 'html',
            success: function(htmlData) {
                // Delete old "more-posts-btn" because a new one will be in htmlData
                // or not if there is no more posts
                $(event.target).parent().remove();

                $('.posts-panel').append(htmlData);
            }
        })
    });
}
