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

function updateProgressBar(progressBarElement, progressBarMessageElement, progress, lenght) {
    progressBarElement.style.width = progress.percent * lenght + "%";
    progressBarMessageElement.innerHTML = progress.percent + '%';
    if (progress.current === progress.total) {
        progressBarElement.style.backgroundColor = "green";
    } else {
        progressBarElement.style.backgroundColor = "#747755";
    }
}

function setBackGround(data) {
    let bar = document.getElementById('progress-bar');
    let barMessage = document.getElementById('progress-bar-message');
    console.log(data.current, data.total, data.message);
    let current = data.current;
    let total = data.total;
    let percent = Math.round((current / total) * 100);
    updateProgressBar(bar, barMessage, {percent: percent, current: percent, total: 100}, 1);

}

function checkInstrument() {
    $.ajax({
            url: '/calib/check',
            type: 'GET',
            success: function (data) {
                console.log(data);
                if (data["msg"] === 0) {
                    lightOnGreen();
                } else
                    lightOnRed();


            },
            error: function () {
            }
        }
    )

}

function get_listfreq() {
    let listfreq;
    let inputFreq = document.getElementById("calibFreq");
    listfreq = inputFreq.value.split(",");
    for (let i = 0; i < listfreq.length; i++) {
        listfreq[i] = parseFloat(listfreq[i]);
    }
    return listfreq;
}

function get_power() {
    let inputPower = document.getElementById("calibPower");
    let power = parseFloat(inputPower.value);
    return power;
}


function calibration() {
    let min = document.getElementById("min");
    let max = document.getElementById("max");
    let rang = document.getElementById("rang");
    let power = get_power();
    $.ajax({
            url: '/calib/calib',
            type: 'GET',
            dataType: 'JSON',
            data: {pwr: power,min:min.value, max:max.value,rang:rang.value},
            success: function (data) {
                document.location.href = "/calib/";
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
            type: 'GET',
            data: {portIN: portIN, portOUT: portOUT, date: date},
            success: function (data) {
                plotLoss(data["freq"], data["loss"]);
            },

            error: function () {

            }

        }
    )
}

function plotLoss(X, Y) {
    let bode = {
        x: X,
        y: Y,
        mode: 'markers',
        type: 'scatter'
    };
    let data = [bode];
    Plotly.newPlot('graph', data);

}


let progressSocket = new WebSocket('ws://' + window.location.host + '/ws/calibprogress/');


progressSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
progressSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    let dataBackEnd = JSON.parse(data['message']);
    setBackGround(dataBackEnd);
    if (dataBackEnd.message !== "") {
                if (confirm(dataBackEnd.message)) {
                    $.ajax({
                        url: "/calib/response",
                        dataType: "JSON",
                        type: "GET",
                        data: {response: 1}
                    })
                }

            }
};

let interval = setInterval(function () {

   progressSocket.send(JSON.stringify({'message': ''}));

}, 500);

lightOff();
