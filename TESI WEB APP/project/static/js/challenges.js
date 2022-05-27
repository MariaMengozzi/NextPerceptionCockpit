$().ready(()=>{
    $('.progress-bar').each(function() {
        //console.log($(this).text())
        $(this).width($(this).text())
    });

    $(".card").click(function() {
        $(this).parent().submit();
    });
})