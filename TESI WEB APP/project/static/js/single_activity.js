function draw_elementOfDistraction() {

    $.ajax({
        url: '/get_elementOfDistraction_data_single_a',
        type: 'POST',
        dataType: 'json',
        data: {'idActivity': $('.idActivity').text()},
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
            let myRadar = document.getElementById("ElementOfDistractionRadar").getContext('2d');

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

//controlla che vada bene
function draw_ftdTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let labels = []

    $.ajax({
        url: '/get_FTD_single_activity',
        type: 'POST',
        dataType: 'json',
        data: {'idActivity': $('.idActivity').text()},
        success: function (dataJSON) {
            dataJSON.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    labels.push(key)
                    data.push(Math.trunc(value*100*100)/100)

                });
            });


            let mychart = document.getElementById("ftdTrendGraph").getContext('2d');

            new Chart(mychart, {
                type: 'line',
                data: {
                    labels: labels,
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
                    scales:{
                        x: {
                            display: false
                        }
                    }
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
            scales:{
                x: {
                    display: false
                }
            }
        }
    });

    $(".ecoTrendMax").text(Math.max(...data))
    $(".ecoTrendMin").text(Math.min(...data))
    $(".ecoTrendMean").text(data.reduce((a, b) => a + b) / data.length)

}

$().ready(() => {
    draw_elementOfDistraction();
    draw_ftdTrend();
    draw_ecoTrend();

    $('.set_like').click(function(){
        $.ajax({
            url: '/set_like',
            type: 'POST',
            data: {'idActivity': $('.idActivity').text()},
            dataType: 'json',
            success: function(res) {
                $('.set_like').prop("disabled",true);
                $('.like_num').text(parseInt($('.like_num').text())+1)
                $('.set_like').empty().html('<ion-icon name="heart" size="small"></ion-icon>')

            },
            error: function () {
                    console.log("error")
            }
        });
    })

    $('form').click(function(){
        $(this).submit();
    })
});