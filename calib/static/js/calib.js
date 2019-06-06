src = "https://code.jquery.com/jquery-3.1.0.min.js";

function lightOnRed() {
    let led1 = document.getElementById('led1');
    led1.style.background = "red";

}

function lightOnGreen() {
    let led1 = document.getElementById('led1');
    led1.style.background = "chartreuse";

}

function lightOff() {
    let led1 = document.getElementById('led1');
    led1.style.background = "transparent";
}

function checkInstrument() {
    $.ajax({
            url: '/calib/check',
            type: 'GET',
            success: function (data) {
                console.log(data);
                lightOnGreen();

            },
            error: function () {
                lightOnRed();
            }
        }
    )

}

function get_listfreq(){
    let listfreq ;
    let inputFreq = document.getElementById("calibFreq");
    listfreq = inputFreq.value.split(",");
    for(let i = 0; i <listfreq.length; i++){
        listfreq[i] = parseFloat(listfreq[i]);
    }
    return listfreq;
}

function get_power(){
    let inputPower = document.getElementById("calibPower");
    let power = parseFloat(inputPower.value);
    return power;
}

function history() {

}

function calibration() {
    let freq = get_listfreq();
    let power = get_power();
    $.ajax({
            url: '/calib/calib',
            type: 'GET',
            dataType: 'JSON',
            data: {pwr:power, freq:JSON.stringify(freq)},
            success: function (data) {
                document.location.href = "/calib/"
            },
            error: function () {
                alert("error ajax");
            }
        }
    );

}
function getLossPath() {
    let calSelect = document.querySelector('#selecthistory');
    let portINSelect = document.querySelector('#portIN');
    let portOUTSelect = document.querySelector('#portOUT');
    let date = calSelect.value;
    let portIN = portINSelect.value;
    let portOUT = portOUTSelect.value;
    $.ajax({
        url: '/calib/getlosspath',
        type:'GET',
        data: {portIN:portIN,portOUT:portOUT,date:date},
        success: function (data) {
            plotLoss(data["freq"],data["loss"]);
        },

        error: function () {

        }

}
    )
}
function plotLoss(X,Y) {
    let bode = {
  x: X,
  y: Y,
  mode: 'markers',
  type: 'scatter'
};
    let data = [bode];
Plotly.newPlot('graph', data);

}


lightOff();
history();