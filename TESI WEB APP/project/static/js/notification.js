function updateListNotification(notifications_list){
    $('.friends_list').empty()
    notifications_list.forEach(n => {
        $('.friends_list').append(`<button type="button" class="btn list-group-item list-group-item-action" id="${n[0]}">
            <p>${n[1]}</p>
            <p>${n[2]}</p>
        </button>`)
    });
}


$().ready(()=>{

    $('.notification_badge').hide()

    $.ajax({
        type: "POST",
        url: "/update_notification",
        dataType: 'json',
        success: function(result) {
            if (result['count'] == 0){
                $('.notification_badge').hide()
            } else{
                $('.notification_badge').show()
                updateListNotification(result['notifications_list'])
            }
       }

    });
    
    $("body").on('click', '.list-group-item', function(){
        element = $(this)
        // cambia nel db e setta visualized a True
        $.ajax({
            type: "POST",
            url: "/read_notification",
            data: {'id_notification': element.attr('id')},
            success: function(html) {
                element.addClass('disabled');
                element.addClass('btn-secondary');
           }

        });
    })

    $(function() {
        setInterval(function() {
            $.ajax({
                type: "POST",
                url: "/update_notification",
                dataType: 'json',
                success: function(result) {
                    if (result['count'] == 0){
                        $('.notification_badge').hide()
                    } else{
                        $('.notification_badge').show()
                        updateListNotification(result['notifications_list'])
                    }
               }

            });
        }, 5000); //ogni 5 sec faccio l'aggiornamento
    }); 
    
    //--> per aggiornare continuamente le notifiche

/*   //verifica se il badge è cambiato, in quel caso allora aggiorna la lista delle notifiche
     $('.notification_badge').on('DOMSubtreeModified',function(){
        let countButton = document.querySelectorAll(".list-group-item").length - document.querySelectorAll(".list-group-item.btn-secondary").length ;
        if (countButton < $(this).text()){
            //console.log("aggiorna lista notifiche");
            //aggiungo i nuovi elementi in alto nella lista 
            //prendo tutte le notifiche - gli id di quelle presenti
            $.ajax({
                url: '/get_all_notification',
                type: "POST",
                data: {"action" : "aggiorna"},
                success: function(result){
                    updateListNotification(result);

                }
            });
        }
      }); */
    
})