$('.query-entry').keypress(function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        var form = $(event.currentTarget).parent();
        var url = form.attr('action');
        var query_text = $(event.currentTarget).attr('value');
        $.post({
            url: url,
            data: {
                query_text: query_text,
                csrfmiddlewaretoken: $('.query-entry').prev().attr('value')
            },
            success: function(htmlData) {
                $('.query-panel').append(htmlData);
            }
        });
    }
});