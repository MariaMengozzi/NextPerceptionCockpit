function draw_elementOfDistraction() {

    $.ajax({
        url: '/get_elementOfDistraction_data',
        type: 'GET',
        dataType: 'json',
        success: function (dataJSON) {
            let color = ['rgb(255, 99, 132)', 'rgb(187, 107, 217)', 'rgb(95, 75, 135)',
                'rgb(244, 108, 100)', 'rgb(211, 142, 133)', 'rgb(162, 69, 255)'];
            let data = [];
            let labels = [];

            //popolare la tabella
            elementColor = 0;
            dataJSON.forEach(obj => {

                Object.entries(obj).forEach(([key, value]) => {
                    //console.log(`${key} ${value}`);

                    labels.push(key);

                    data.push(Math.trunc(value*100*100)/100);
 
                    $(".elementOfDistractionTable tbody").append(`<tr>
                    <th scope="row" id="${key}" headers="disctractionElement">${key}</th>
                    <td headers="distractionValue ${key}">${Math.trunc(value*100*100)/100}</td>
                    <td headers="distractionColor ${key}" style="background: ${color[elementColor]};"></td>
                    </tr>`);
                    elementColor += 1
                });
                //console.log('-------------------');
                
            });
            ftd = Math.trunc((100 - data.reduce((a, b) => a + b ,0))*100)/100
            $(".elementOfDistractionTable tbody").append(`<tr>
                    <th scope="row" id="ftd" headers="disctractionElement">FTD</th>
                    <td headers="distractionValue ftd">${ftd}</td>
                    <td headers="distractionColor ${ftd}" style="background: ${color[3]};"></td>
                    </tr>`);

            labels.push('FTD')
            data.push(ftd)

            //la creazione dei grafici devo metterla dentro al success sennò li crea senza dati
            let myPie = document.getElementById("ElementOfDistractionPie").getContext('2d');

            new Chart(myPie, {
                type: 'pie',
                data: {
                    datasets: [{
                        label: 'Element of distraction',
                        data: data,
                        backgroundColor: color,
                        hoverOffset: 3
                    }]
                },
                options: {
                    aspectRatio: 1.5 //(width/height)
                }
            });

            let myRadar = document.getElementById("ElementOfDistractionRadar").getContext('2d');

            new Chart(myRadar, {
                type: 'radar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Element of distraction',
                        data: data,
                        fill: true,
                        backgroundColor: 'rgb(255, 99, 132,0.2)',
                        borderColor: '#d63384',
                        pointBackgroundColor: '#d63384',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#d63384'
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
                            },
                            pointLabels: {
                                color: 'white'
                            }
                        }
                    }
                }
            });

        },
        error: function () {
            console.log("error")
        }
    });


    /* let color = [
        'rgb(255, 99, 132)',
        'rgb(187, 107, 217)',
        'rgb(95, 75, 135)'
    ];

    let data = []; //[20, 35, 45] //prendere da db

    let distraction = [
        { "elementName": "A", "elementValue": 20 },
        { "elementName": "B", "elementValue": 35 },
        { "elementName": "C", "elementValue": 45 }
    ]

    //popolare la tabella
    distraction.forEach(obj => {
        elementName = ''
        elementValue = 0
        Object.entries(obj).forEach(([key, value]) => {
            //console.log(`${key} ${value}`);
            if (key == "elementValue") {
                elementValue = value;
                data.push(value)
            } else {
                elementName = value;
            }
        });
        //console.log('-------------------');
        $(".elementOfDistractionTable tbody").append(`<tr>
        <th scope="row" id="${elementName}" headers="disctractionElement">${elementName}</th>
        <td headers="distractionValue ${elementName}">${elementValue}</td>
        <td headers="distractionColor ${elementName}"></td>
        </tr>`)
    }); */



    $('#ElementOfDistractionRadar').toggle();

}

//controlla che vada bene
function draw_ftdTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let days = []

    $.ajax({
        url: '/get_last_10_FTD',
        type: 'GET',
        dataType: 'json',
        success: function (dataJSON) {
            dataJSON.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {

                    if (key == "giorno") {
                        days.push(value)
                    } else {
                        data.push(value)
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
                        borderColor: 'rgb(187, 107, 217)',
                        tension: 0.1,
                        backgroundColor: 'rgba(187, 107, 217, 0.2)'
                    }]
                },
                options: {
                    aspectRatio: 1.5, //(width/height)
                    scales: {
                        x: {
                            ticks: {
                                color: 'white'
                            },
                            grid: {
                                color: '#1c5b97'
                            }
                        },
                        y: {
                            ticks: {
                                color: 'white'
                            },
                            grid: {
                                color: '#1c5b97'
                            }
                        },
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

/* function draw_ecoTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let days = []
    let ecoTrend = [
        { "day": "2021-02-15", "val": 45 },
        { "day": "2021-05-15", "val": 4 },
        { "day": "2021-04-15", "val": 50 },
        { "day": "2021-04-18", "val": 25 }
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
                borderColor: 'rgb(187, 107, 217)',
                tension: 0.1,
                backgroundColor: 'rgba(187, 107, 217, 0.2)'
            }]
        },
        options: {
            aspectRatio: 1.5, //(width/height)
            scales: {
                x: {
                    ticks: {
                        color: 'white'
                    },
                    grid: {
                        color: '#1c5b97'
                    }
                },
                y: {
                    ticks: {
                        color: 'white'
                    },
                    grid: {
                        color: '#1c5b97'
                    }
                },
            }
        }
    });

    $(".ecoTrendMax").text(Math.max(...data))
    $(".ecoTrendMin").text(Math.min(...data))
    $(".ecoTrendMean").text(data.reduce((a, b) => a + b) / data.length)

} */

$().ready(() => {
    draw_elementOfDistraction();
    draw_ftdTrend();
    //draw_ecoTrend()

    $("button#showPie").on("click", function () {
        $(this).prop("disabled", true);
        $("button#showRadar").prop("disabled", false);
        $('#ElementOfDistractionRadar').toggle();
        $('#ElementOfDistractionPie').toggle();

    });

    $("button#showRadar").on("click", function () {
        $(this).prop("disabled", true);
        $("button#showPie").prop("disabled", false);
        $('#ElementOfDistractionRadar').toggle();
        $('#ElementOfDistractionPie').toggle();
    })
});