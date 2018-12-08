$('.delete-post-confirm-window').click(function(event) {
    event.stopPropagation();
})

$(".delete-post-background").click(function(event) {
    $(".delete-post-background").remove();
});

$('.cancel-btn').click(function(event) {
    $('.delete-post-background').remove();
});


