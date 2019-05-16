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

function get_listPorts() {
    let listPorts = [];
    let checkboxInput = document.querySelectorAll("#portIN");
    for (let i = 0; i < checkboxInput.length; i++) {
        if (checkboxInput[i].checked === true) {
            listPorts.push(checkboxInput[i].name);
        }
    }
    return listPorts;
}

function get_listChannels() {
    let listChannels = [];
    let checkboxChannels = document.querySelectorAll("#portOUT");
    for (let i = 0; i < checkboxChannels.length; i++) {
        if (checkboxChannels[i].checked === true) {
            listChannels.push(checkboxChannels[i].name);
        }
    }
    return listChannels;
}

function get_parametersSwitchCalibration() {

}

function get_parametersWiresCalibration() {
    let pwr = document.getElementById("calibWirePower").value;
    let freq = document.getElementById("calibWireFreq").value;
    let channels = get_listChannels();
    let ports = get_listPorts();

    return {'pwr':pwr,'freq': freq,'ports': ports,'channels': channels}

}



function calibration() {
    $.ajax({
            url: '/calib/calib',
            type: 'GET',
            success: function (data) {

            },
            error: function () {
                alert("error ajax");
            }
        }
    );

}



lightOff();