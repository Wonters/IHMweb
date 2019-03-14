src="https://code.jquery.com/jquery-3.1.0.min.js"

function updateProgressBar(progressBarElement, progressBarMessageElement, progress, lenght) {
    progressBarElement.style.width = progress.percent * lenght + "%";
    progressBarMessageElement.innerHTML = progress.current + ' of ' + progress.total + ' processed.';
    if (progress.current === progress.total) {
        progressBarElement.style.backgroundColor = "green";
    }

}

function moreChannel(event) {
    var select_channel = document.querySelector('#channel');
    var newchannel = select_channel.cloneNode(true);
    var div = document.querySelector('#channels');
    div.insertBefore(newchannel, document.querySelector("#addchannel"));
}

function lessChannel(event) {
    var div = document.querySelector('#channels');
    var delchan = div.firstChild;
    if (delchan.id !== 'addchannel') {
        div.removeChild(delchan);
    }
}

function sendschedule() {
    var list = {};
    var temperature = document.querySelector('#temperature');
    var delay = document.querySelector('#delay');
    var checkbox = document.querySelectorAll("#content");
    for (var i = 0; i < checkbox.length; i++) {
        list[checkbox[i].name] = checkbox[i].checked;
    }
    var data_json = JSON.stringify(list);
    $.ajax({
            url: '/testcase/writeschedule' ,
            type: 'GET',
            dataType: 'json',
            data: {tc2play: data_json, temperature: temperature.value, delay: delay.value},
            success: function () {
                showCommand();
            },
            error: function () {
                alert("Error ajax");
            }
        }
    )
}

function setBackGround() {
    var bar = document.getElementById('progress-bar');
    var barMessage = document.getElementById('progress-bar-message');
    var listProgressTc = document.querySelectorAll('.progresstc');
    $.ajax({
        url: '{% url "counter" %}',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var tc_name = data.tc;
            var temp = data.temperature;
            var current = data.current;
            var total = data.total;
            var percent = Math.round((current / total) * 100);
            var tc_current = data.tc_current;
            var tc_total = data.tc_total;
            var tc_percent = Math.round((tc_current / tc_total) * 100);
            setTimeout(function () {
                whereAreYouScheduler(tc_name, {percent: tc_percent, current: tc_percent, total: 100}, temp)
            }, 100);
            updateProgressBar(bar, barMessage, {percent: percent, current: percent, total: 100}, 0.5);


            if (current !== total || total === 0) {
                setTimeout(function () {
                    setBackGround();
                }, 500);
            }
            if (current === total) {
                current = 0;
                total = 0;
            }
        },
        error: function (data) {
            alert("Error ajax");
        }
    });
}

function whereAreYouScheduler(name, progress, temperature) {
    var bar = document.querySelector('#progress-bar-tc');
    var message = document.querySelector('#progress-bar-message-tc');
    var p = document.querySelector('#name-tc');
    var pTemperature = document.querySelector('#which-temperature');
    p.innerHTML = name;
    pTemperature.innerHTML = temperature;
    updateProgressBar(bar, message, progress, 0.33);

}

function startProgress() {

    setBackGround();
}


function showCommand() {
    DivCommand = document.getElementById("commande");
    DivCommand.style.visibility = "visible";

}

function hiddenCommand() {
    DivCommand = document.getElementById("commande");
    DivCommand.style.visibility = "hidden";

}

