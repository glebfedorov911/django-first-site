$(document).ready(function() {
    $('#comment_form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: "",
            data: {
                comment_text: $('#id_text').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data) {
                $(".comments").load(location.href + " .comments");
                $(".pag").load(location.href + " .pag");
                $("#comment_form")[0].reset();
            }
        });
    });
});

setInterval(() => $(".comments").load(location.href + " .comments"), 2000)