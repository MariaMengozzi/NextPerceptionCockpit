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

$().ready(()=>{

    setInterval(function(){
        $.ajax({
            url: '/get_cockpit_data',
            type: 'GET',
            dataType: 'json',
            success: function(dataJSON) {
                console.log(dataJSON.id)
                updateSpeedGauge(dataJSON.vehicleSpeed)
                updateRPMGauge(dataJSON.engineSpeed)
                updateFuel(dataJSON.fuelLevel)
            },
            error: function () {
                    console.log("error")
            }
        });
    }, 5000);  //change to 50

});