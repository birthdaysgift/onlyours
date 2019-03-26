function toCenterVertical(CssSelector) {
    var size = ($(window).height() - $(CssSelector).height())/2;
    $(CssSelector).css('margin-top', size + 'px');

}

$(document).ready(function() {
    toCenterVertical('.container');
})

$(window).resize(function(event) {
    toCenterVertical('.container');
})
