var size = ($(window).height() - $('.container').height())/2;
$('.container').css('margin-top', size + 'px');

$(window).resize(function(event) {
    var size = ($(window).height() - $('.container').height())/2;
    $('.container').css('margin-top', size + 'px');
})
