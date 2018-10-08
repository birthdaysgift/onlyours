$(".friends-text").click( function(event) {
    var url = $(".friends-list-link").attr("href");
    $.get({
        url: url,
        dataType: "html",
        success: function(htmlData) {
            $(".wrapper").prepend(htmlData);
        }
    });
});

