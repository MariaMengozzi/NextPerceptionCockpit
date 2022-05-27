function draw_elementOfDistraction() {
    
    $.ajax({
        url: '/get_elementOfDistraction_data',
        type: 'GET',
        dataType: 'json',
        success: function (dataJSON) {
            let color = ['rgb(255, 99, 132)','rgb(187, 107, 217)','rgb(95, 75, 135)',
                            'rgb(244, 108, 100)','rgb(211, 142, 133)', 'rgb(162, 69, 255)'];
            let data = [];
            let labels = [];
            //qui popolare color e data va a sostiturire  dove distraction è dataJSON

            //popolare la tabella
            elementColor = 0;
            dataJSON.forEach(obj => {
                elementName = ''
                elementValue = 0
                elementColor += 1 //''
                Object.entries(obj).forEach(([key, value]) => {
                    //console.log(`${key} ${value}`);
                    if (key == "value") {
                        elementValue = value;
                        data.push(value)
                    } else if (key == "name") {
                        elementName = value;
                        labels.push(value)
                    } else {
                        elementColor = value;
                        color.push(value)
                    }
                });
                //console.log('-------------------');
                $(".elementOfDistractionTable tbody").append(`<tr>
                    <th scope="row" id="${elementName}" headers="disctractionElement">${elementName}</th>
                    <td headers="distractionValue ${elementName}">${elementValue}</td>
                    <td headers="distractionColor ${elementName}" style="background: ${color[elementColor]};"></td>
                    </tr>`);
            });

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

function draw_ftdTrend() {
    let data = []; //[20, 35, 45] //prendere da db
    let days = []
    let ftdTrend = [
        { "day": "2021-02-15", "val": 20 },
        { "day": "2021-05-15", "val": 35 },
        { "day": "2021-04-15", "val": 45 },
        { "day": "2021-04-18", "val": 25 }
    ]

    //popolare la tabella
    ftdTrend.forEach(obj => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key == "val") {
                data.push(value)
            } else {
                days.push(value)
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

    $(".ftdTrendMax").text(Math.max(...data))
    $(".ftdTrendMin").text(Math.min(...data))
    $(".ftdTrendMean").text(data.reduce((a, b) => a + b) / data.length)

}

function draw_ecoTrend() {
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

}

$().ready(() => {
    draw_elementOfDistraction();
    draw_ftdTrend();
    draw_ecoTrend()

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