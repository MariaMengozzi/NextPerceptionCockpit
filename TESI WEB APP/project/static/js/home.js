$().ready(()=>{
    $(".card").click(function() {
        $(this).parent().submit();
    });
})