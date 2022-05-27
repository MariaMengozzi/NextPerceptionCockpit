var eco_level = 0;
var ftd_level = 0;

function updateTree(mod) {
  var bb = treePath.getBBox()
  var bby = bb.y
  var bbh = bb.height
  //---bottom of heart---
  var base = bby + bbh

  if (eco_level < 1 && mod =='up') {
    eco_level += .05
  } else if (eco_level > 0 && mod =='down'){
    eco_level -= .05
  }
  var percent = (1 - eco_level) * base;
  $("#treeRect").attr("y", percent)
  $('p').text('Eco drive level: ' + parseInt(eco_level*100) + '%')
}

function updateEcoGauge(mod){
  if(mod != ''){
    eco_level = mod == 'up'? eco_level + .05 : eco_level-.05
  }
  $('#gaugeEco').empty();
    
    Gauge(
      document.getElementById("gaugeEco"), {
      max: 100,
      value: parseInt(eco_level * 100),
      unit: '',
      unity: function (unit) { return unit; },
      dialStartAngle: 0,
      dialEndAngle: 180,
      label: function (value) {
        return Math.round(value * 100) / 100 + '%';
      }
    }
    );
    $('.containerDisplaySection').append(
      `<div> <button id='incrEcoVal'>incrEcoVal</button>
    <button id='decrEcoVal'>decrEcoVal</button></div>`);
}

//aggiungi chiamata a messaggio d'allarme se il livello di ftd < SOGLIA
function updateFtd(mod) {
  var bb = ftdPath.getBBox()
  var bby = bb.y
  var bbh = bb.height
  //---bottom of heart---
  var base = bby + bbh

  if (ftd_level < 1 && mod =='up') {
    ftd_level += .05
  } else if (ftd_level > 0 && mod =='down'){
    ftd_level -= .05
  }
  var percent = (1 - ftd_level) * base;
  $("#ftdRect").attr("y", percent)
  $('p').text('Fitness to drive level: ' + parseInt(ftd_level*100) + '%')
}

function updateFtdGauge(mod){
  if(mod != ''){
    ftd_level = mod == 'up'? ftd_level + .05 : ftd_level-.05
  }
  $('#gaugeFtd').empty();
    
    Gauge(
      document.getElementById("gaugeFtd"), {
      max: 100,
      value: parseInt(ftd_level * 100),
      unit: '',
      unity: function (unit) { return unit; },
      dialStartAngle: 0,
      dialEndAngle: 180,
      label: function (value) {
        return Math.round(value * 100) / 100 + '%';
      }
    }
    );
    $('.containerDisplaySection').append(
      `<div><button id='incrFtdVal'>incrFtdVal</button>
    <button id='decrFtdVal'>decrFtdVal</button></div>`);
}



function updateFTD_value(ftd_value, ftdVisible){

  if (ftdVisible){
    var bb = ftdPath.getBBox()
    var bby = bb.y
    var bbh = bb.height
    //---bottom of heart---
    var base = bby + bbh

    var percent = (1-ftd_value) * base;
    $("#ftdRect").attr("y", percent)
    $('p').text('Fitness to drive level: ' + parseInt(ftd_value*100) + '%')
  }
  else {
    $('#gaugeFtd').empty();
      
      Gauge(
        document.getElementById("gaugeFtd"), {
        max: 100,
        value: parseInt(ftd_value * 100),
        unit: '',
        unity: function (unit) { return unit; },
        dialStartAngle: 0,
        dialEndAngle: 180,
        label: function (value) {
          return Math.round(value * 100) / 100 + '%';
        }
      }
      );
      $('.containerDisplaySection').append(
        `<div><button id='incrFtdVal'>incrFtdVal</button>
      <button id='decrFtdVal'>decrFtdVal</button></div>`);
  }
}

$(document).ready(() => {
  var fuel_level = 30;
  var water_level = 80;
  //var treeVisible = false;
  //var ecoGaugeVisible = false;
  var ftdGaugeVisible = false;
  var ftdVisible = false;

  setInterval(function(){
    $.ajax({
        url: '/getFTD',
        type: 'GET',
        dataType: 'json',
        success: function(dataJSON) {
          updateFTD_value(dataJSON.ftd, ftdVisible)
        },
        error: function () {
                console.log("error")
        }
    });
}, 100);

  $(".msgAlarm").hide();
  $(".msgSaving").hide();

  $(".btShowFtd").on("click", () => {
    ftdVisible = !ftdVisible
    if (ftdVisible) { 
      if(ftdGaugeVisible){
        $('.btShowFtdGauge').click()
      }
      //Eco drive tree
      $('.containerDisplaySection').append(`<p class="text-white">Fitness to drive level: 0% </p>
    <svg version="1.1" id="ftdSVG" xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="-5 -5 568.031 568.03"
        style="enable-background:new 0 -1  568.031 568.03;" xml:space="preserve">
        <defs>
            <mask id="ftd">
            <g>
            <path d="M 256 0.5 C 193.691 0.5 143 51.191 143 113.5 C 143 148.508 159.00217 179.8478 184.07617 200.5918 C 141.08017 215.6958 103.47791 244.37695 77.378906 283.37695 C 71.235906 292.55695 73.696953 304.97809 82.876953 311.12109 C 86.293953 313.40809 90.157469 314.50195 93.980469 314.50195 C 100.43047 314.50195 106.76409 311.38605 110.62109 305.62305 C 142.93809 257.33105 196.96181 228.5 255.13281 228.5 C 313.13181 228.5 367.0643 257.19853 399.4043 305.26953 C 405.5713 314.43453 417.99811 316.86522 427.16211 310.69922 C 436.32711 304.53322 438.75975 292.10541 432.59375 282.94141 C 406.75475 244.53541 369.70705 216.19711 327.37305 201.03711 C 352.76105 180.29811 369 148.761 369 113.5 C 369 51.191 318.309 0.5 256 0.5 z M 256 40.5 C 296.252 40.5 329 73.248 329 113.5 C 329 153.752 296.252 186.5 256 186.5 C 215.748 186.5 183 153.752 183 113.5 C 183 73.248 215.748 40.5 256 40.5 z M 256.00195 279.5 C 250.92995 279.5 245.85789 282.39459 243.96289 288.18359 L 232.57422 323.21094 C 230.88022 328.38894 226.02111 330.5 220.53711 330.5 L 183.68359 330.5 C 171.42159 330.5 166.32219 347.47486 176.24219 354.63086 L 206.05859 376.13867 C 210.49459 379.33867 212.35125 385.01145 210.65625 390.18945 L 198.66016 424.99219 C 198.15316 426.54119 197.95472 428.056 198.01172 429.5 C 198.38372 438.847 210.15409 445.24097 218.74609 439.04297 L 248.56055 417.52734 C 250.77855 415.92734 253.39095 415.12891 256.00195 415.12891 C 258.61295 415.12891 261.22341 415.92734 263.44141 417.52734 L 293.25586 439.04297 C 301.84786 445.24097 313.56328 438.847 313.98828 429.5 C 314.05328 428.056 313.85856 426.54219 313.35156 424.99219 L 301.34375 390.18945 C 299.64875 385.01145 301.50541 379.33867 305.94141 376.13867 L 335.75781 354.63086 C 345.67781 347.47486 340.57936 330.5 328.31836 330.5 L 291.46484 330.5 C 285.98084 330.5 281.12273 328.38894 279.42773 323.21094 L 268.03906 288.18359 C 266.14406 282.39459 261.07395 279.5 256.00195 279.5 z M 85 349.5 C 79.928 349.5 74.857891 352.39459 72.962891 358.18359 L 61.574219 393.21094 C 59.880219 398.38894 55.019156 400.5 49.535156 400.5 L 12.681641 400.5 C 0.41964063 400.5 -4.6778125 417.47486 5.2421875 424.63086 L 35.058594 446.13867 C 39.494594 449.33867 41.35125 455.01145 39.65625 460.18945 L 27.660156 494.99219 C 27.153156 496.54119 26.952766 498.056 27.009766 499.5 C 27.381766 508.847 39.152141 515.24097 47.744141 509.04297 L 77.560547 487.52734 C 79.778547 485.92734 82.389 485.12891 85 485.12891 C 87.611 485.12891 90.221453 485.92734 92.439453 487.52734 L 122.25586 509.04297 C 130.84786 515.24097 142.56328 508.847 142.98828 499.5 C 143.05328 498.056 142.85856 496.54219 142.35156 494.99219 L 130.34375 460.18945 C 128.64875 455.01145 130.50541 449.33867 134.94141 446.13867 L 164.75781 424.63086 C 174.67781 417.47486 169.58036 400.5 157.31836 400.5 L 120.46484 400.5 C 114.98084 400.5 110.12078 398.38894 108.42578 393.21094 L 97.037109 358.18359 C 95.142109 352.39459 90.072 349.5 85 349.5 z M 427.00195 349.5 C 421.92995 349.5 416.85789 352.39459 414.96289 358.18359 L 403.57422 393.21094 C 401.88022 398.38894 397.02111 400.5 391.53711 400.5 L 354.68359 400.5 C 342.42159 400.5 337.32219 417.47486 347.24219 424.63086 L 377.05859 446.13867 C 381.49459 449.33867 383.35125 455.01145 381.65625 460.18945 L 369.66016 494.99219 C 369.15316 496.54119 368.95472 498.056 369.01172 499.5 C 369.38372 508.847 381.15409 515.24097 389.74609 509.04297 L 419.56055 487.52734 C 421.77855 485.92734 424.39095 485.12891 427.00195 485.12891 C 429.61295 485.12891 432.22341 485.92734 434.44141 487.52734 L 464.25586 509.04297 C 472.84786 515.24097 484.56328 508.847 484.98828 499.5 C 485.05328 498.056 484.85856 496.54219 484.35156 494.99219 L 472.34375 460.18945 C 470.64875 455.01145 472.50541 449.33867 476.94141 446.13867 L 506.75781 424.63086 C 516.67781 417.47486 511.57936 400.5 499.31836 400.5 L 462.46484 400.5 C 456.98084 400.5 452.12273 398.38894 450.42773 393.21094 L 439.03906 358.18359 C 437.14406 352.39459 432.07395 349.5 427.00195 349.5 z "/>
            </g>
            <filter id="glow">
              <fegaussianblur class="blur" result="coloredBlur" stddeviation="4"></fegaussianblur>
              <femerge>
                <femergenode in="coloredBlur"></femergenode>
                <femergenode in="coloredBlur"></femergenode>
                <femergenode in="coloredBlur"></femergenode>
                <femergenode in="SourceGraphic"></femergenode>
              </femerge>
            </mask>
        </defs>
        <rect id=ftdRect x=0 y="100%" width="100%" height="100%" mask="url(#ftd)" />
        <g>
        <path id='ftdPath' filter="url(#glow)" d="M 256 0.5 C 193.691 0.5 143 51.191 143 113.5 C 143 148.508 159.00217 179.8478 184.07617 200.5918 C 141.08017 215.6958 103.47791 244.37695 77.378906 283.37695 C 71.235906 292.55695 73.696953 304.97809 82.876953 311.12109 C 86.293953 313.40809 90.157469 314.50195 93.980469 314.50195 C 100.43047 314.50195 106.76409 311.38605 110.62109 305.62305 C 142.93809 257.33105 196.96181 228.5 255.13281 228.5 C 313.13181 228.5 367.0643 257.19853 399.4043 305.26953 C 405.5713 314.43453 417.99811 316.86522 427.16211 310.69922 C 436.32711 304.53322 438.75975 292.10541 432.59375 282.94141 C 406.75475 244.53541 369.70705 216.19711 327.37305 201.03711 C 352.76105 180.29811 369 148.761 369 113.5 C 369 51.191 318.309 0.5 256 0.5 z M 256 40.5 C 296.252 40.5 329 73.248 329 113.5 C 329 153.752 296.252 186.5 256 186.5 C 215.748 186.5 183 153.752 183 113.5 C 183 73.248 215.748 40.5 256 40.5 z M 256.00195 279.5 C 250.92995 279.5 245.85789 282.39459 243.96289 288.18359 L 232.57422 323.21094 C 230.88022 328.38894 226.02111 330.5 220.53711 330.5 L 183.68359 330.5 C 171.42159 330.5 166.32219 347.47486 176.24219 354.63086 L 206.05859 376.13867 C 210.49459 379.33867 212.35125 385.01145 210.65625 390.18945 L 198.66016 424.99219 C 198.15316 426.54119 197.95472 428.056 198.01172 429.5 C 198.38372 438.847 210.15409 445.24097 218.74609 439.04297 L 248.56055 417.52734 C 250.77855 415.92734 253.39095 415.12891 256.00195 415.12891 C 258.61295 415.12891 261.22341 415.92734 263.44141 417.52734 L 293.25586 439.04297 C 301.84786 445.24097 313.56328 438.847 313.98828 429.5 C 314.05328 428.056 313.85856 426.54219 313.35156 424.99219 L 301.34375 390.18945 C 299.64875 385.01145 301.50541 379.33867 305.94141 376.13867 L 335.75781 354.63086 C 345.67781 347.47486 340.57936 330.5 328.31836 330.5 L 291.46484 330.5 C 285.98084 330.5 281.12273 328.38894 279.42773 323.21094 L 268.03906 288.18359 C 266.14406 282.39459 261.07395 279.5 256.00195 279.5 z M 85 349.5 C 79.928 349.5 74.857891 352.39459 72.962891 358.18359 L 61.574219 393.21094 C 59.880219 398.38894 55.019156 400.5 49.535156 400.5 L 12.681641 400.5 C 0.41964063 400.5 -4.6778125 417.47486 5.2421875 424.63086 L 35.058594 446.13867 C 39.494594 449.33867 41.35125 455.01145 39.65625 460.18945 L 27.660156 494.99219 C 27.153156 496.54119 26.952766 498.056 27.009766 499.5 C 27.381766 508.847 39.152141 515.24097 47.744141 509.04297 L 77.560547 487.52734 C 79.778547 485.92734 82.389 485.12891 85 485.12891 C 87.611 485.12891 90.221453 485.92734 92.439453 487.52734 L 122.25586 509.04297 C 130.84786 515.24097 142.56328 508.847 142.98828 499.5 C 143.05328 498.056 142.85856 496.54219 142.35156 494.99219 L 130.34375 460.18945 C 128.64875 455.01145 130.50541 449.33867 134.94141 446.13867 L 164.75781 424.63086 C 174.67781 417.47486 169.58036 400.5 157.31836 400.5 L 120.46484 400.5 C 114.98084 400.5 110.12078 398.38894 108.42578 393.21094 L 97.037109 358.18359 C 95.142109 352.39459 90.072 349.5 85 349.5 z M 427.00195 349.5 C 421.92995 349.5 416.85789 352.39459 414.96289 358.18359 L 403.57422 393.21094 C 401.88022 398.38894 397.02111 400.5 391.53711 400.5 L 354.68359 400.5 C 342.42159 400.5 337.32219 417.47486 347.24219 424.63086 L 377.05859 446.13867 C 381.49459 449.33867 383.35125 455.01145 381.65625 460.18945 L 369.66016 494.99219 C 369.15316 496.54119 368.95472 498.056 369.01172 499.5 C 369.38372 508.847 381.15409 515.24097 389.74609 509.04297 L 419.56055 487.52734 C 421.77855 485.92734 424.39095 485.12891 427.00195 485.12891 C 429.61295 485.12891 432.22341 485.92734 434.44141 487.52734 L 464.25586 509.04297 C 472.84786 515.24097 484.56328 508.847 484.98828 499.5 C 485.05328 498.056 484.85856 496.54219 484.35156 494.99219 L 472.34375 460.18945 C 470.64875 455.01145 472.50541 449.33867 476.94141 446.13867 L 506.75781 424.63086 C 516.67781 417.47486 511.57936 400.5 499.31836 400.5 L 462.46484 400.5 C 456.98084 400.5 452.12273 398.38894 450.42773 393.21094 L 439.03906 358.18359 C 437.14406 352.39459 432.07395 349.5 427.00195 349.5 z "/>
      </g>
    </svg>
    <br> 
    <button id='fillFTD'>fillFTD</button>
    <button id='unfillFTD'>unfillFTD</button>`)
      updateFtd('');
      //togliere br!
      $('.containerDisplaySection').fadeIn("slow");
    } else {
      $('.containerDisplaySection').fadeOut("slow");
      $('.containerDisplaySection').empty();
    }
  });

  $('.btShowFtd').click()

  $(".btShowFtdGauge").on("click", () => {
    ftdGaugeVisible = !ftdGaugeVisible
    if (ftdGaugeVisible) {
      if( ftdVisible){
        $(".btShowFtd").click()
      }

      $('.containerDisplaySection').addClass("gauge-container ftd");
      $('.containerDisplaySection').attr('id', 'gaugeFtd')
      //$('.containerDisplaySection').append('<div id="gaugeEco" class="gauge-container eco"><p class="text-white">Eco drive level</p></div>');
      updateFtdGauge('')

      $('.containerDisplaySection').fadeIn("slow");
    } else {
      $('.containerDisplaySection').fadeOut("slow");
      $('.containerDisplaySection').removeClass("gauge-container eco");
      $('.containerDisplaySection').removeAttr('id', 'gaugeFtd')
      $('.containerDisplaySection').empty();
    }
  });


  $("body").on('click', '#fillFTD', function () {
    updateFtd('up');
  });

  $("body").on('click', '#unfillFTD', () => {
    updateFtd('down');
  });

  $("body").on('click', '#decrFtdVal', function () {
    updateFtdGauge('down')
  });

  $("body").on('click', '#incrFtdVal', () => {
    updateFtdGauge('up')
  });

  $(".fuel").css('width', fuel_level + '%');
  $(".fuel").text(fuel_level + '%');

  $(".water").css('width', water_level + '%');
  $(".water").text(water_level + '%');

  $('.btShowAlarm').on("click", ()=>{
    if( $('.msgSaving').is(':hidden')){
      $('.containerDisplaySection').hide();
      $('.msgAlarm').fadeIn('slow', function(){
        $('.msgAlarm').delay(5000).fadeOut(function(){
          $('.containerDisplaySection').fadeIn();
        }); 
      });
    }
  });

  $('.btShowSavings').on("click", ()=>{
    if( $('.msgAlarm').is(':hidden')){
      $('.containerDisplaySection').hide();
      $('.msgSaving').fadeIn('slow', function(){
        $('.msgSaving').delay(5000).fadeOut(function(){
          $('.containerDisplaySection').fadeIn();
        }); 
      });
    }
    
  });

  /*   $("#fillTree").on("click", function () {
      https://stackoverflow.com/questions/42672537/how-to-animate-fill-instead-of-path-in-an-svg-progress-bar
      var bb = treePath.getBBox()
      var bby = bb.y
      var bbh = bb.height
      //---bottom of heart---
      var heartBase = bby + bbh
  
      if (level < 1) {
        level += .05
        var percent = (1 - level) * heartBase;
        $("#treeRect").attr("y", percent)
      }
  
      var iT = setInterval(donate, 50 )  
        var Donations=0
          function donate()
          {
               if(level>=1) {
                 clearInterval(iT);
               }
              var bb=treePath.getBBox()
              var bby=bb.y
              var bbh=bb.height
              //---bottom of heart---
              var heartBase=bby+bbh
          
              if(level<1)
              {
                level+=.05
                  var percent=(1-level)*heartBase;
                  $("#treeRect").attr("y",percent)
              }
          } 
    }); */

  /*   $("#unfillTree").on("click", function () {
      var bb = treePath.getBBox()
      var bby = bb.y
      var bbh = bb.height
      //---bottom of heart---
      var heartBase = bby + bbh
  
      if (level >0) {
        level -= .05
        var percent = (1 - level) * heartBase;
        $("#treeRect").attr("y", percent)
      }
      setInterval(donate, 50)
      var Donations = 1
      function donate() {
        var bb = treePath.getBBox(); //return the actual bounding box at the time the method was called
        var bby = bb.y;
        var bbh = bb.height;
        //---bottom of heart---
        var heartBase = bby + bbh;
  
        if (Donations > 0) {
          Donations -= .05
          var percent = (1 - Donations) * heartBase;
          $("#treeRect").attr("y", percent);
        }
      }
    }); */

  Gauge(
    document.getElementById("gaugeSpeed"), {
    max: 200,
    value: 0,
    unit: 'km/h',
    unity: function (unit) { return unit; },
    dialStartAngle: 90,
    dialEndAngle: -60,
    label: function (value) {
      return Math.round(value * 100) / 100;
    }

  }
  );

  Gauge(
    document.getElementById("gaugeRPM"), {
    max: 10,
    dialStartAngle: 90,
    dialEndAngle: -60,
    value: 2,
    unit: 'RPM',
    unity: function (unit) { return unit; },
    label: function (value) {
      return Math.round(value * 100) / 100;
    }
  }
  );

  /*   $('input').on("input", function () {
      $('#gaugeSpeed').empty();
      val = $(this).val();
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
    }); */



});