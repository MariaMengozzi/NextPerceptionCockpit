function draw_level_stars() {
    //get form ajax call level value
    $('.single_star').hide()
    let level = parseInt($('.level').text())
    for (let index = 0; index < level; index++) {
        $('.single_star_full_' + index).show()
    }

    level_i = level
    while (level_i != 5) {
        $('.single_star_empty_' + level_i).show()
        level_i++
    }
}

function draw_donuts() {

    ftdRES = parseFloat($('.global_FTD_score').text())
    new Chart(document.getElementById("FTD-donuts").getContext('2d'), {
        type: 'doughnut',
        data: {
            labels:['FTD Result'],
            datasets: [{
                data: [ftdRES, (100- ftdRES)],
                backgroundColor: ['#178FD6',
                '#C4C4C4'],
                hoverOffset: 3
            }]
        },
        options: {
            aspectRatio: 1.5 //(width/height)
        }
    });

    ecoRES = 85
    new Chart(document.getElementById("ECO-donuts").getContext('2d'), {
        type: 'doughnut',
        data: {
            labels:['ECO Result'],
            datasets: [{
                data: [ecoRES, (100- ecoRES)],
                backgroundColor: ['#4AA626',
                '#C4C4C4'],
                hoverOffset: 3
            }]
        },
        options: {
            aspectRatio: 1.5 //(width/height)
        }
    });
    //$('.eco_best_results').text(ecoRES)
}

function draw_elementOfDistractionMean() {
    
    $.ajax({
        url: '/get_elementOfDistraction_data',
        type: 'POST',
        dataType: 'json',
        data: {'nick': $('.profile_nickname').text().trim()},
        success: function (dataJSON) {
            let data = [];
            let labels = [];

            //popolare la tabella
            dataJSON.forEach(obj => {

                Object.entries(obj).forEach(([key, value]) => {
                    //console.log(`${key} ${value}`);
                    if(['DV', 'DC', 'emotion'].includes(key)){
                        labels.push(key);

                        data.push(Math.trunc(value*100*100)/100);
     
                        $(".elementOfDistractionTable tbody").append(`<tr>
                        <th scope="row" id="${key}" headers="disctractionElement">${key}</th>
                        <td headers="distractionValue ${key}">${Math.trunc(value*100*100)/100}</td>
                        </tr>`);
                    }
                    
                });
                //console.log('-------------------');
                
            });
            ftd = Math.trunc((100 - data.reduce((a, b) => a + b ,0))*100)/100
            $(".elementOfDistractionTable tbody").append(`<tr>
                    <th scope="row" id="ftd" headers="disctractionElement">FTD</th>
                    <td headers="distractionValue ftd">${ftd}</td>
                    </tr>`);

            labels.push('FTD')
            data.push(ftd)

            //la creazione dei grafici devo metterla dentro al success sennò li crea senza dati
            let myRadar = document.getElementById("ElementOfDistractionRadarMean").getContext('2d');

            new Chart(myRadar, {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Element of distraction',
                        data: data,
                        fill: true,
                        backgroundColor: '#8ab8f544',
                        borderColor: '#2F80ED',
                        pointBackgroundColor: '#1471eb',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#1471eb'
                    }]
                },
                options: {
                    aspectRatio: 1.5, //(width/height)
                    elements: {
                        line: {
                            borderWidth: 3
                        }
                    },
                    scales: {
                        r: {
                            grid: {
                                color: '#1c5b97'
                            }
                        }
                    }
                }
            });

        } ,
        error: function () {
            console.log("error")
        }
    });
}

function draw_ftdTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let days = []

    $.ajax({
        url: '/get_last_10_FTD',
        type: 'POST',
        dataType: 'json',
        data: {'nick': $('.profile_nickname').text().trim()},
        success: function (dataJSON) {
            dataJSON.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {

                    if (key == "giorno") {
                        days.push(value)
                    } else if (key =='ftd') {
                        data.push(Math.trunc(value*100*100)/100)
                    }
                });
            });


            let mychart = document.getElementById("ftdTrendGraph").getContext('2d');

            new Chart(mychart, {
                type: 'line',
                data: {
                    labels: days,
                    datasets: [{
                        label: 'ftd trend',
                        data: data,
                        fill: true,
                        borderColor: '#2F80ED',
                        tension: 0.1,
                        backgroundColor: '#8ab8f544'
                    }]
                },
                options: {
                    aspectRatio: 1.5, //(width/height)
                }
            });

            $(".ftdTrendMax").text(Math.trunc(Math.max(...data)*100)/100)
            $(".ftdTrendMin").text(Math.trunc(Math.min(...data)*100)/100)
            $(".ftdTrendMean").text(Math.trunc((data.reduce((a, b) => a + b) / data.length)*100)/100)
        },
        error: function () {
            console.log("error")
        }
    });
}

function draw_ecoTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let days = []
    let ecoTrend = [
        { "day": "2021-02-15", "val": 45 },
        { "day": "2021-05-15", "val": 4 },
        { "day": "2021-04-15", "val": 50 },
        { "day": "2021-04-18", "val": 25 },
        { "day": "2021-02-19", "val": 45 }
    ]

    //popolare la tabella
    ecoTrend.forEach(obj => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key == "val") {
                data.push(value)
            } else {
                days.push(value)
            }
        });
    });


    let mychart = document.getElementById("ecoTrendGraph").getContext('2d');

    new Chart(mychart, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                label: 'eco trend',
                data: data,
                fill: true,
                borderColor: '#219653',
                tension: 0.1,
                backgroundColor: '#96e8ba44'
            }]
        },
        options: {
            aspectRatio: 1.5, //(width/height)
/*             scales: {
                x: {
                    grid: {
                        color: '#1c5b97'
                    }
                },
                y: {
                    grid: {
                        color: '#1c5b97'
                    }
                },
            } */
        }
    });

    $(".ecoTrendMax").text(Math.max(...data))
    $(".ecoTrendMin").text(Math.min(...data))
    $(".ecoTrendMean").text(data.reduce((a, b) => a + b) / data.length)

}

function draw_ftdAndEcoBarPlot(){

    $.ajax({
        url: '/get_last_10_FTD',
        type: 'POST',
        dataType: 'json',
        data: {'nick': $('.profile_nickname').text().trim()},
        success: function (dataJSON) {
            
            const data = {
                labels: [],
                datasets: [{
                  type: 'bar',
                  label: 'FTD Data',
                  data: [],
                  borderColor: '#B1E7FE',
                  backgroundColor: '#B1E7FE'
                }, {
                  type: 'bar',
                  label: 'Eco Data',
                  data: [45, 4, 50, 25, 45],
                  borderColor: '#CDECA9',
                  backgroundColor: '#CDECA9'
                }]
              };

            dataJSON.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {

                    if (key == "giorno") {
                        data['labels'].push(value)
                    } else if (key =='ftd') {
                        data['datasets'][0]['data'].push(Math.trunc(value*100*100)/100)
                    }
                });
            });

            var ftdAndEcoBarPlot = new Chart(document.getElementById("ftdAndEcoBarPlot").getContext('2d'), {
                type: 'bar',
                data: data,
                options: {
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }
             });
        },
        error: function () {
            console.log("error")
        }
    });

}


$().ready(() => {

    draw_level_stars();
    draw_donuts();
    draw_elementOfDistractionMean();
    draw_ftdTrend();
    draw_ecoTrend();
    draw_ftdAndEcoBarPlot();

    $('.nav-tabs > a').click(function () {

        $('.nav-tabs > a').removeClass('active').attr('aria-selected', 'false')
        $(this).addClass('active').attr('aria-selected', 'true')

        $('.tab-pane').removeClass('show').removeClass('active')

        classe = "." + $(this).attr('aria-controls')
        $(classe).addClass('show').addClass('active')
    });


    $("form").click(function() {
        $(this).submit();
    });

    $('.btn-amicizia').on('click', function(){
        
        //chiamata ajax per aggiungere l'amicizia
        $.ajax({
            url: '/add_friend',
            type: 'POST',
            data: {'nick': $('.profile_nickname').text().trim()},
            dataType: 'json',
            success: function(res) {
                $('.btn-amicizia').prop("disabled",true);
                $('.friends_num').text(parseInt($('.friends_num').text())+1)
            },
            error: function () {
                    console.log("error")
            }
        });
    })

    $(".friends_num").click(function(){
    	$(".blur").css("filter",'blur(5px)');
        $('.hover_bkgr_fricc').show();
    });
    $('.hover_bkgr_fricc').click(function(){
    	$(".blur").css("filter",'');
        $('.hover_bkgr_fricc').hide();
    });
    $('.popupCloseButton').click(function(){
    	$(".blur").css("filter",'');
        $('.hover_bkgr_fricc').hide();
    });

    $('table >tbody > tr').click(function(){
        id = $(this).find(':first').attr('id')
        text = $(this).find(':first').text()
        id_c = id.replace("_"+text,'')
        console.log(id_c)
        $(function() {
            $('<form action="/single_challenge" method="post"><input type="hidden" name="idChallenge" value="'+id_c+'"></input></form>').appendTo('body').submit().remove();
         });
     
         /* $.ajax({
            url: '/single_challenge',
            type: 'POST',
            data: {'idChallenge': parseInt(id_c)},
            success: function (res){

            }, error:function(){
                console.log('error change page')
            }
        }); */
    });

})