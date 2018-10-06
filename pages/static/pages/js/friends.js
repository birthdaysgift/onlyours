$(".friends-text").click( function() {
    var url = $(".friends-list-link").attr("href");
    $.get({
        url: url,
        dataType: "html",
        success: function (htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    });
});

