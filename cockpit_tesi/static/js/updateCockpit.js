function updateSpeedGauge(speed_val){
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

function updateRPMGauge(RPM_val){
    $('#gaugeRPM').empty();
    val = RPM_val/1000
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

function updateFuel(fuel_level){
    level = parseInt(fuel_level)
    $(".fuel").css('width', level +'%');
    $(".fuel").text(level +'%');
}

function updateValues(data){
  $(".cognitiveDistractionVal").text(data.cognitiveDistraction)
  $(".visualDistractionVal").text(data.visualDistraction)

  $(".neutralVal").text(data.neutral)
  $(".angryVal").text(data.angry)
  $(".joyVal").text(data.joy)
  $(".fearVal").text(data.fear)
  $(".sadnessVal").text(data.sadness)
  $(".disgustVal").text(data.disgust)
  $(".surpriseVal").text(data.surprise)

  $(".arousalVal").text(data.arousal)
}


//si occupa di chiamare ogni secondo lo script che fa la publish dei messaggi contenenti i dati 
$().ready(()=>{

    setInterval(function(){
        $.ajax({
            url: '/publish_data',
            type: 'GET',
            dataType: 'json',
            success: function(dataJSON) {
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

    setInterval(function(){
      $.ajax({
          url: '/getFTD',
          type: 'GET',
          dataType: 'json',
          success: function(dataJSON) {
            $(".FTDVal").text(dataJSON.ftd)
          },
          error: function () {
                  console.log("error")
          }
      });
  }, 1000);  //change to 1000 == 1 sec -> 50 millisec == 20hz

});