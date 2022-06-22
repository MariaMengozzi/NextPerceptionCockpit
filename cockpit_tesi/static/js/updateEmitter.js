let anger_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let happiness_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let fear_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let sadness_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let neutral_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let disgust_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let surprise_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let speed_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let cognitive_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let visual_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let visual = 0
let arousal_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let ftd_buffer = [0, 0, 0, 0, 0, 0, 0, 0]

let ftdChart = new Chart(document.getElementById("ftdChart").getContext('2d'), {
    type: 'line',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'FTD',
            data: ftd_buffer,
            borderColor: 'rgb(189, 191, 9)',
            tension: 0.3,
        }
        ]
    },
    options: {
        animation: {
            duration: 0
        },
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
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

let emotionChart = new Chart(document.getElementById("emotionLinechart").getContext('2d'), {
    type: 'line',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'anger',
            data: anger_buffer,
            borderColor: 'rgb(172, 189, 186)',
            tension: 0.3,
        },
        {
            label: 'happiness',
            data: happiness_buffer,
            borderColor: 'rgb(232, 180, 188)',
            tension: 0.3,
        },
        {
            label: 'disgust',
            data: disgust_buffer,
            borderColor: 'rgb(113, 231, 188)',
            tension: 0.3,
        },
        {
            label: 'fear',
            data: fear_buffer,
            borderColor: 'rgb(194, 29, 188)',
            tension: 0.3,
        },
        {
            label: 'neutral',
            data: neutral_buffer,
            borderColor: 'rgb(176, 202, 135)',
            tension: 0.3,
        },
        {
            label: 'surprise',
            data: surprise_buffer,
            borderColor: 'rgb(168, 130, 221)',
            tension: 0.3,
        },
        {
            label: 'sadness',
            data: sadness_buffer,
            borderColor: 'rgb(238, 252, 87)',
            tension: 0.3,
        },
        ]
    },
    options: {
        animation: {
            duration: 0
        },
        //aspectRatio: 1.5, //(width/height)
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
        },
        //options.plugins.legend.labels
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

let speedChart = new Chart(document.getElementById("speedLineChart").getContext('2d'), {
    type: 'line',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'speed',
            data: speed_buffer,
            borderColor: 'rgb(249, 86, 79)',
            tension: 0.3,
        }
        ]
    },
    options: {
        animation: {
            duration: 0
        },
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
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

let arousalChart = new Chart(document.getElementById("arousalChart").getContext('2d'), {
    type: 'line',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'arousal',
            data: arousal_buffer,
            borderColor: 'rgb(34, 146, 164)',
            tension: 0.3,
        }
        ]
    },
    options: {
        animation: {
            duration: 0
        },
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
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

let cdChart = new Chart(document.getElementById("cognitiveDistractionChart").getContext('2d'), {
    type: 'bar',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'cognitiveDistraction',
            data: cognitive_buffer,
            backgroundColor: 'rgba(170, 246, 131, 0.2)',
            borderColor: 'rgb(170, 246, 131)'
        }
        ]
    },
    options: {
        animation: {
            duration: 0
        },
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
                },
                beginAtZero: true
            },
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

let vdChart = new Chart(document.getElementById("visualDistractionChart").getContext('2d'), {
    type: 'bar',
    data: {
        labels: ["", "", "", "", "", "", "", ""],
        datasets: [{
            label: 'visualDistraction',
            data: visual_buffer,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgb(153, 102, 255)',
        }
        ]
    },
    options: {
        animation: {
            duration: 0
        },
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
                },
                beginAtZero: true
            },
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            }
        }
    }
});

function emotionLineChart() {
    emotionChart.data.datasets = [{
        label: 'anger',
        data: anger_buffer,
        borderColor: 'rgb(172, 189, 186)',
        tension: 0.3,
    },
    {
        label: 'happiness',
        data: happiness_buffer,
        borderColor: 'rgb(232, 180, 188)',
        tension: 0.3,
    },
    {
        label: 'disgust',
        data: disgust_buffer,
        borderColor: 'rgb(113, 231, 188)',
        tension: 0.3,
    },
    {
        label: 'fear',
        data: fear_buffer,
        borderColor: 'rgb(194, 29, 188)',
        tension: 0.3,
    },
    {
        label: 'neutral',
        data: neutral_buffer,
        borderColor: 'rgb(176, 202, 135)',
        tension: 0.3,
    },
    {
        label: 'surprise',
        data: surprise_buffer,
        borderColor: 'rgb(168, 130, 221)',
        tension: 0.3,
    },
    {
        label: 'sadness',
        data: sadness_buffer,
        borderColor: 'rgb(238, 252, 87)',
        tension: 0.3,
    }
    ]
    emotionChart.update()
}

function speedLineChart() {
    speedChart.data.datasets = [{
        label: 'speed',
        data: speed_buffer,
        borderColor: 'rgb(249, 86, 79)',
        tension: 0.3,
    },
    ]
    speedChart.update()
}

function ftdLineChart() {
    ftdChart.data.datasets = [{
        label: 'FTD',
        data: ftd_buffer,
        borderColor: 'rgb(189, 191, 9)',
        tension: 0.3,
    },
    ]
    ftdChart.update()
}

function arousalLineChart() {
    arousalChart.data.datasets = [{
        label: 'arousal',
        data: arousal_buffer,
        borderColor: 'rgb(34, 146, 164)',
        tension: 0.3,
    },
    ]
    arousalChart.update()
}

function cdBarChart() {
    cdChart.data.datasets = [{
        label: 'cognitiveDistraction',
        data: cognitive_buffer,
        backgroundColor: 'rgba(170, 246, 131, 0.2)',
        borderColor: 'rgb(170, 246, 131)'
    }
    ]
    cdChart.update()
}

function vdBarChart() {
    vdChart.data.datasets = [{
        label: 'visualDistraction',
        data: visual_buffer,
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgb(153, 102, 255)',
    }
    ]
    vdChart.update()
}

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("Emotions");
    client.subscribe("RL_VehicleDynamics");
    client.subscribe("NP_UNITO_DCDC");
    client.subscribe("AITEK_EVENTS");
    client.subscribe("NP_UNIBO_FTD");
    client.subscribe("NP_UNIPR_AROUSAL")
}

//called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

// called when a message arrives
function onMessageArrived(message) {

    if (message.destinationName === "Emotions") {
        json = ''
        if (message.payloadString.length === 0 || message.payloadString === "{}"){
            json = '{"person0": {"predominant" : "0","neutral":"0","happiness": "0","surprise":"0","sadness": "0","anger": "0","disgust": "0","fear": "0","engagement": "0","valence": "0"}}'
        } else {
            json = message.payloadString
        }

        msg = JSON.parse(json)

        anger_buffer.shift()
        anger_buffer.push(parseFloat(msg.person0.anger))

        happiness_buffer.shift()
        happiness_buffer.push(parseFloat(msg.person0.happiness))

        neutral_buffer.shift()
        neutral_buffer.push(parseFloat(msg.person0.neutral))

        fear_buffer.shift()
        fear_buffer.push(parseFloat(msg.person0.fear))

        disgust_buffer.shift()
        disgust_buffer.push(parseFloat(msg.person0.disgust))

        sadness_buffer.shift()
        sadness_buffer.push(parseFloat(msg.person0.sadness))

        surprise_buffer.shift()
        surprise_buffer.push(parseFloat(msg.person0.surprise))

        $(".angryVal").text(msg.person0.anger)
        $(".neutralVal").text(msg.person0.neutral)
        $(".joyVal").text(msg.person0.happiness)
        $(".fearVal").text(msg.person0.fear)
        $(".sadnessVal").text(msg.person0.sadness)
        $(".disgustVal").text(msg.person0.disgust)
        $(".surpriseVal").text(msg.person0.surprise)
        emotionLineChart()
    } else if (message.destinationName === "RL_VehicleDynamics") {
        msg = JSON.parse(message.payloadString)
        speed_buffer.shift()
        speed_buffer.push(parseFloat(msg.VehicleDynamics.speed.x))
        $(".speedVal").text(msg.VehicleDynamics.speed.x)
        speedLineChart()
    } else if (message.destinationName === "NP_UNITO_DCDC") {
        json = ""
        if (message.payloadString.length === 0){
            json = '{"cognitive_distraction" : 0}'
        } else {
            json = message.payloadString
        }
        msg = JSON.parse(json)
        cognitive_buffer.shift()
        cognitive_buffer.push(parseInt(msg.cognitive_distraction))
        $(".cognitiveDistractionVal").text(msg.cognitive_distraction)
        cdBarChart()
    } else if (message.destinationName === "NP_UNIBO_FTD") {
        msg = JSON.parse(message.payloadString)
        $(".FTDVal").text(msg.person0.ftd)
        visual_buffer.shift()
        visual_buffer.push(parseInt(visual))

        ftd_buffer.shift()
        ftd_buffer.push(parseFloat(msg.person0.ftd))
        ftdLineChart()
    } else if (message.destinationName === "AITEK_EVENTS") {
        msg = JSON.parse(message.payloadString)
        visual = msg.start === 'True' ? 1 : 0
        visual_buffer.shift()
        visual_buffer.push(visual)
        $(".visualDistractionVal").text(msg.start)
        vdBarChart()
    } else if (message.destinationName === "NP_UNIPR_AROUSAL") {
        msg = JSON.parse(message.payloadString)
        arousal_buffer.shift()
        arousal_buffer.push(parseFloat(msg.arousal))
        $(".arousalVal").text(msg.arousal)
        arousalLineChart()
    }
}


//si occupa di chiamare ogni secondo lo script che fa la publish dei messaggi contenenti i dati 
$().ready(() => {
    //mqtt docs: https://www.eclipse.org/paho/index.php?page=clients/js/index.php
    // Create a client instance
    client = new Paho.MQTT.Client('broker.mqttdashboard.com', 8000, "ftdCockpit");

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // connect the client
    client.connect({ onSuccess: onConnect });

    //create charts
    emotionChart
    speedChart
    cdChart
    vdChart
    arousalChart
    ftdChart
});
