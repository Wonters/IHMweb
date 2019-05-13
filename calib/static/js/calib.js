src = "https://code.jquery.com/jquery-3.1.0.min.js";

function lightOnRed() {
    let led1 = document.getElementById('led1');
    led1.style.background ="red";

}

function lightOnGreen() {
    let led1 = document.getElementById('led1');
    led1.style.background ="chartreuse";

}

function lightOff() {
    let led1 = document.getElementById('led1');
    led1.style.background ="transparent";
}

function checkInstrument() {
    $.ajax({
        url:'/calib/check',
        type:'GET',
        success: function () {
            lightOnGreen();

        },
        error: function () {
            lightOnRed();
        }
        }
    )

}

lightOff();
