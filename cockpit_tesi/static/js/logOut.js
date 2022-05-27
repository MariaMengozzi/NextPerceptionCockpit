$(function () {
    $(window).bind("beforeunload", function () {
        $.ajax({
            url: '/logout',
            type: 'GET',
            success: function(data) {
                console.log('ok')
            },
            error: function () {
                    console.log("error")
            }
        });

    })
});
