function updateSpeedGauge(speed_val) {
  $('#gaugeSpeed').empty();
  val = speed_val
  Gauge(
    document.getElementById("gaugeSpeed"), {
    max: 200,
    value: parseInt(val),
    unit: 'km/h',
    unity: function (unit) { return unit; },
    dialStartAngle: 90,
    dialEndAngle: -60,
    label: function (value) {
      return Math.round(value * 100) / 100;
    }
  });
}

function updateRPMGauge(RPM_val) {
  $('#gaugeRPM').empty();
  val = RPM_val / 1000
  Gauge(
    document.getElementById("gaugeRPM"), {
    max: 10,
    dialStartAngle: 90,
    dialEndAngle: -60,
    value: parseInt(val),
    unit: 'RPM',
    unity: function (unit) { return unit; },
    label: function (value) {
      return Math.round(value * 100) / 100;
    }
  }
  );
}

function updateFuel(fuel_level) {
  level = parseInt(fuel_level)
  $(".fuel").css('width', level + '%');
  $(".fuel").text(level + '%');
}


let anger_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let happiness_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let fear_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let sadness_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let neutral_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let disgust_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let surprise_buffer = [0, 0, 0, 0, 0, 0, 0, 0]
let speed_buffer = [0, 0, 0, 0, 0, 0, 0, 0]

let emotionChart = new Chart(document.getElementById("emotionLinechart").getContext('2d'), {
  type: 'line',
  data: {
    labels: ["", "", "", "", "", "", "", ""],
    datasets: [{
      label: 'anger',
      data: anger_buffer,
      borderColor: 'rgb(172, 189, 186)',
      tension: 0.1,
    },
    {
      label: 'happiness',
      data: happiness_buffer,
      borderColor: 'rgb(232, 180, 188)',
      tension: 0.1,
    },
    {
      label: 'disgust',
      data: disgust_buffer,
      borderColor: 'rgb(113, 231, 188)',
      tension: 0.1,
    },
    {
      label: 'fear',
      data: fear_buffer,
      borderColor: 'rgb(194, 29, 188)',
      tension: 0.1,
    },
    {
      label: 'neutral',
      data: neutral_buffer,
      borderColor: 'rgb(176, 202, 135)',
      tension: 0.1,
    },
    {
      label: 'surprise',
      data: surprise_buffer,
      borderColor: 'rgb(168, 130, 221)',
      tension: 0.1,
    },
    {
      label: 'sadness',
      data: sadness_buffer,
      borderColor: 'rgb(238, 252, 87)',
      tension: 0.1,
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
    }
  }
});

function emotionLineChart() {
  emotionChart.data.datasets =  [{
    label: 'anger',
    data: anger_buffer,
    borderColor: 'rgb(172, 189, 186)',
    tension: 0.1,
  },
  {
    label: 'happiness',
    data: happiness_buffer,
    borderColor: 'rgb(232, 180, 188)',
    tension: 0.1,
  },
  {
    label: 'disgust',
    data: disgust_buffer,
    borderColor: 'rgb(113, 231, 188)',
    tension: 0.1,
  },
  {
    label: 'fear',
    data: fear_buffer,
    borderColor: 'rgb(194, 29, 188)',
    tension: 0.1,
  },
  {
    label: 'neutral',
    data: neutral_buffer,
    borderColor: 'rgb(176, 202, 135)',
    tension: 0.1,
  },
  {
    label: 'surprise',
    data: surprise_buffer,
    borderColor: 'rgb(168, 130, 221)',
    tension: 0.1,
  },
  {
    label: 'sadness',
    data: sadness_buffer,
    borderColor: 'rgb(238, 252, 87)',
    tension: 0.1,
  }
  ]
  emotionChart.update()
}

function updateValues(data) {
  $(".cognitiveDistractionVal").text(data.cognitiveDistraction)
  $(".visualDistractionVal").text(data.visualDistraction)

  $(".arousalVal").text(data.arousal)
  $(".speedVal").text(data.vehicleSpeed)
}


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("Emotions");
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
    msg = JSON.parse(message.payloadString)
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
  }
}


//si occupa di chiamare ogni secondo lo script che fa la publish dei messaggi contenenti i dati 
$().ready(() => {
  setInterval(function () {
    $.ajax({
      url: '/publish_data',
      type: 'GET',
      dataType: 'json',
      success: function (dataJSON) {
        //console.log(dataJSON.id)
        updateSpeedGauge(dataJSON.vehicleSpeed)
        //updateRPMGauge(dataJSON.engineSpeed)
        //updateFuel(dataJSON.fuelLevel)
        updateValues(dataJSON)
      },
      error: function () {
        console.log("error")
      }
    });
  }, 1000);  //change to 1000 == 1 sec -> 50 millisec == 20hz

  setInterval(function () {
    $.ajax({
      url: '/getFTD',
      type: 'GET',
      dataType: 'json',
      success: function (dataJSON) {
        $(".FTDVal").text(dataJSON.ftd)
      },
      error: function () {
        console.log("error")
      }
    });
  }, 1000);  //change to 1000 == 1 sec -> 50 millisec == 20hz

  //mqtt docs: https://www.eclipse.org/paho/index.php?page=clients/js/index.php
  // Create a client instance
  client = new Paho.MQTT.Client('broker.mqttdashboard.com', 8000, "ftdCockpit");

  // set callback handlers
  client.onConnectionLost = onConnectionLost;
  client.onMessageArrived = onMessageArrived;

  // connect the client
  client.connect({ onSuccess: onConnect });

  emotionChart
});