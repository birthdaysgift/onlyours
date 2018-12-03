$('.username-input').focusin(function(event) {
    $('.username-info').animate({
        height: "62px"
    }, {
        duration: 200,
        start: function() {
            $(".username-info-text").css("display", "block");
        }
    })
});

$('.username-input').focusout(function(event) {
    $('.username-info').animate({
        height: "42"
    }, {
        duration: 200,
        start: function() {
            $(".username-info-text").css("display", "none");
        }
    })
});

$('.password-input').focusin(function(event) {
    $('.password-info').animate({
        height: "62px"
    }, {
        duration: 200,
        start: function() {
            $(".password-info-text").css("display", "block");
        }
    })
})

$('.password-input').focusout(function(event) {
    $('.password-info').animate({
        height: "42px"
    }, {
        duration: 200,
        start: function() {
            $(".password-info-text").css("display", "none");
        }
    })
})

$('.confirm-input').focusin(function(event) {
    $('.confirm-info').animate({
        height: "62px"
    }, {
        duration: 200,
        start: function() {
            $(".confirm-info-text").css("display", "block");
        }
    })
})

$('.confirm-input').focusout(function(event) {
    $('.confirm-info').animate({
        height: "42px"
    }, {
        duration: 200,
        start: function() {
            $(".confirm-info-text").css("display", "none");
        }
    })
})

$(document).ready(function(event) {
    var size = ($(window).height() - $('.container').height())/2;
    $('.container').css('margin-top', size + 'px');
})

$(window).resize(function(event) {
    var size = ($(window).height() - $('.container').height())/2;
    $('.container').css('margin-top', size + 'px');
})
