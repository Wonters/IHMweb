function updateProgressBar(progressBarElement, progressBarMessageElement, progress, lenght, color) {
    progressBarElement.style.width = progress.percent * lenght + "%";
    progressBarMessageElement.innerHTML = progress.percent + '%';
    if (progress.current === progress.total) {
        progressBarElement.style.backgroundColor = "green";
    } else {
        progressBarElement.style.backgroundColor = color;
    }
}

function get_listChannels() {
    let label_temp = document.querySelector('#channels');
    let listTemp = label_temp.value.split(',').map(parseFloat);
    if (isNaN(listTemp[0])) {
        listTemp = [];
    }
    return listTemp
}

function nbrChannel() {

    let listchannels = get_listChannels();
    return listchannels.length;
}

function moreChannel(event) {
    if (nbrChannel() < 8) {
        let select_channel = document.querySelector('#channel');
        let label_channels = document.querySelector('#channels');
        let newchannel = select_channel.value;
        let list_channels = get_listChannels();
        list_channels.push(newchannel);
        label_channels.value = list_channels.toString();
    }
}

function lessChannel(event) {
    let label_channels = document.querySelector('#channels');
    let listchannels = get_listChannels();
    if (nbrChannel() > 0) {
        listchannels.pop();
        label_channels.value = listchannels;
    }
}

function get_listTemperature() {
    let label_temp = document.querySelector('#temperature');
    let listTemp = label_temp.value.split(',').map(parseFloat);
    if (isNaN(listTemp[0])) {
        listTemp = [];
    }
    return listTemp
}

function moreTemperature(event) {
    let label_temp = document.querySelector('#temperature');
    let new_temp = document.querySelector("#temp");
    let listTemp = get_listTemperature();
    listTemp.push(new_temp.value);
    label_temp.value = listTemp.toString();
}

function lessTemperature(event) {
    let listtemp = get_listTemperature();
    let label_temp = document.querySelector('#temperature');
    if (listtemp.length > 0) {
        listtemp.pop();
        label_temp.value = listtemp;
    }

}

function plotSchedule(listTc) {
    let divScheduler = document.querySelector('.scheduler');
    let HTMLcollection = divScheduler.getElementsByClassName('listTc');
    if (HTMLcollection.length !== 0) {
        for (let i = 0, len = HTMLcollection.length; i < len; i++) {
            HTMLcollection[i].remove();
        }
    }

    let divListTc = document.createElement('div');
    divListTc.setAttribute('class', 'listTc');

    for (let mode in listTc) {
        if (listTc[mode].length !== 0) {
            let divMode = document.createElement('div');
            divMode.className = "testcase";
            divMode.id = 'scheduler_' + mode;
            let label = document.createElement('label');
            label.innerText = mode;
            divMode.appendChild(label);
            for (let i = 0; i < listTc[mode].length; i++) {
                $.ajax({
                        url: '/carac/readtc',
                        type: 'GET',
                        dataType: 'json',
                        data: {tc: i + ',' + mode},
                        success: function (data_return) {
                            let divTc = document.createElement('div');
                            let tc_label = document.createElement('label');
                            let checkbox = document.createElement('input');

                            divTc.className = ""; // bootstrap

                            tc_label.name = 'testcase';
                            tc_label.className = "h4";
                            tc_label.id = "";
                            tc_label.for = 'checkbox-large';
                            tc_label.setAttribute('data-toggle', "tooltip");
                            tc_label.setAttribute('data-placement', 'bottom');
                            tc_label.setAttribute('title', JSON.stringify(data_return['testcase']));

                            if (data_return['testcase']['name'] === '') {
                                tc_label.innerText = 'noname';
                            } else {
                                tc_label.innerText = data_return['testcase']['name'];
                            }

                            checkbox.name = i + ',' + mode;
                            checkbox.type = "checkbox";
                            checkbox.id = "checkbox-large";
                            checkbox.checked = true;
                            //checkbox.className ='custom-control-input';
                            checkbox.style = 'width: 20px; height: 20px';

                            divTc.appendChild(checkbox);
                            divTc.appendChild(tc_label);
                            divMode.appendChild(divTc);
                        },
                        error: function () {
                            alert("Error ajax");
                        }
                    }
                );
            }
            divListTc.appendChild(divMode);
        }
    }
    divScheduler.appendChild(divListTc);
} // plot the campagn of testcases availables

function showTempSetting() {
    let climCham = document.getElementById('climChamber').value;
    let tempSetting = document.getElementById('tempSetting');
    if (climCham === 'yes') {
        tempSetting.style.visibility = 'visible';
    } else {
        tempSetting.style.visibility = 'hidden';
    }

}

function showNewCampagn() {
    let div_newCampagn = document.getElementById('campagn_new');
    if (div_newCampagn.style.visibility === 'hidden') {
        div_newCampagn.style.visibility = 'visible';
    } else {
        div_newCampagn.style.visibility = 'hidden';
    }
    document.getElementById('tempSetting').style.visibility = 'hidden';
}

function sendSchedule(event) {
    let list = {};
    let listTemp = JSON.stringify(get_listTemperature());
    let delay = document.querySelector('#delay');
    let checkbox = document.querySelectorAll("#checkbox-large");
    let climCham = document.getElementById('climChamber').value;

    if (climCham === "no"){
        listTemp = JSON.stringify([25]);
    }

    for (let i = 0; i < checkbox.length; i++) {
        list[checkbox[i].name] = checkbox[i].checked;
    }

    let data_json = JSON.stringify(list);
    if (Object.keys(list).length === 0) {
        alert("please select a configuration and testcases to play")
    }
    else {
        $.ajax({
                url: '/carac/writeschedule',
                type: 'GET',
                dataType: 'json',
                data: {tc2play: data_json, temperature: listTemp, delay: delay.value},
                success: function () {
                    startcarac();
                },
                error: function () {
                    alert("Error ajax to send scheduler");
                }
            }
        );
    }
}

function startcarac() {
    let name = document.getElementById('name').value;
    let type = document.getElementById('type').value;
    let simulate = document.getElementById('simulated').value;
    let climCham = document.getElementById('climChamber').value;
    let channels = document.getElementById('channels').value;
    let baseStation = document.getElementById('baseStation').value;

    if (confirm("Warning : are you sure to have" + baseStation)) {
        $.ajax({
            type: 'GET',
            url: '/carac/start',
            data: {nameCarac: name, simulate: simulate, climChamber: climCham, channel: channels, type: type},
            success: function (data) {
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
        });
    }

}

function checkState(state) {
    let start_button = document.getElementById('cmd-button-start');
    let stop_button = document.getElementById('cmd-button-stop');
    if (state === 'running') {
        start_button.disabled = true;
        stop_button.disabled = false;
    }

    if (state === 'success' || state === 'ready' || state === 'abort') {
        start_button.disabled = false;
        stop_button.disabled = true;
    }

}

function setBackGround(data) {
    let bar = document.getElementById('progress-bar');
    let barMessage = document.getElementById('progress-bar-message');
    console.log(data['state']);
    let state = data.state;
    let response = data.responseTask;
    let tc_name = data.tc;
    let temp = data.temperature;
    let current = data.current;
    let total = data.total;
    let percent = Math.round((current / total) * 100);
    let tc_current = data.tc_current;
    let tc_total = data.tc_total;
    let tc_percent = Math.round((tc_current / tc_total) * 100);
    let name = data.name;
    let channels = data.channels;
    let date = data.date;
    let climstate = data.clim;
    let climcurrent = data.clim_current;
    let climtotal = data.clim_total;
    let percentclim = Math.round((climcurrent / climtotal) * 100);
    let tc2play = data.tc2play;
    let templist = data.templist;
    let type = data.type;
    checkState(response);
    if (total != 0) {
        updateProgressBar(bar, barMessage, {percent: percent, current: percent, total: 100}, 1, "#447e9b");
        whereAreYouScheduler(tc_name, {
            percent: tc_percent,
            current: tc_percent,
            total: 100
        }, temp, {current: tc_current, total: tc_total}, date, channels, name, climstate, {
            percent: percentclim,
            current: percentclim,
            total: 100
        }, templist, tc2play, type);
    }
}

function whereAreYouScheduler(tc, progressTc, temperature, iteration, date, channels, name, climstate, progressClim, templist, tc2play, type) {
    let bar = document.querySelector('#progress-bar-tc');
    let message = document.querySelector('#progress-bar-message-tc');
    let barclim = document.querySelector("#progress-bar-clim");
    let messageclim = document.querySelector('#progress-bar-message-clim');
    let p = document.querySelector('#name-tc');
    let pIteration = document.querySelector('#iteration-mesure');
    let pTemperature = document.querySelector('#which-temperature');
    let pname = document.querySelector('#pname');
    let pchannels = document.querySelector('#pchannels');
    let pdate = document.querySelector('#pdate');
    let pclim = document.querySelector('#pclimchamber');
    let ptemplist = document.querySelector('#ptemplist');
    let ptc2play = document.querySelector('#ptc2play');
    let ptype = document.querySelector('#ptype');
    p.innerHTML = tc;
    pname.innerHTML = name;
    ptype.innerHTML = type;
    pchannels.innerHTML = channels;
    pdate.innerHTML = date;
    pclim.innerHTML = climstate;
    ptemplist.innerHTML = templist;
    ptc2play.innerHTML = tc2play;
    pTemperature.innerHTML = temperature;
    pIteration.innerHTML = iteration.current + '/' + iteration.total;
    updateProgressBar(bar, message, progressTc, 1, "#747755");
    updateProgressBar(barclim, messageclim, progressClim, 1, " #993300");


}

function startProgress(event) {
    sendSchedule();
}

function stopProgress(event) {
    $.ajax({
        url: '/carac/stop',
        success: function (data) {

        },
        error: function (data) {
            console.log('An error occurred.');
            console.log(data);
        },
    });
}

function loadConf(value, event) {
    $.ajax({
        url: '/carac/load',
        dataType: 'json',
        type: 'GET',
        data: {configname: value},
        success: function s(data) {
            plotSchedule(data.listTc);
        },
        error: function e() {
            alert("Error ajax");
        },
    })
}


showTempSetting();
showNewCampagn();

let progressSocket = new WebSocket('ws://' + window.location.host + '/ws/progress/');

progressSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

progressSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    setBackGround(JSON.parse(data['message']));
};

let interval = setInterval(function () {
    progressSocket.send(JSON.stringify({'message': ''}));
}, 500);