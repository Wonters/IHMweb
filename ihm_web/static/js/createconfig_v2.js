let field = ['bbFreq2', 'bbFreq1', 'bbFreqCal', 'inputAttCal', 'inputAtt', 'refLvl', 'rbw', 'vbw',
    'span', 'countAverage', 'pwmeter', 'searchLimit', 'name', 'radio_configuration'];

let radioMode = ["rc1","rc2","rc3","rc4", "rc5", "rc6"];

function createTab(parameter, element) {
    let tab = [];
    let nbiteration = (Number(parameter.max) - Number(parameter.min)) / Number(parameter.rang);
    for (let i = 0; i <= nbiteration; i++) {
        tab[i] = Number(parameter.min) + i * Number(parameter.rang);
    }
    element.value = tab.join();
}

function createRange(balise) {
    let pas = document.createElement('input');
    let min = document.createElement('input');
    let max = document.createElement('input');
    let generate = document.createElement('button');
    pas.id = "pas";
    min.id = "min";
    max.id = "max";
    generate.id = 'button';
    pas.setAttribute('class', ' input1');
    min.setAttribute('class', ' input1');
    max.setAttribute('class', ' input1');
    generate.setAttribute('class', ' btn btn-info');
    pas.type = 'number';
    min.type = 'number';
    max.type = 'number';
    pas.min = 1;
    generate.innerText = "auto";

    const list = [min, max, pas, generate];
    generate.addEventListener("click", function e() {
        createTab({
            min: list[0].value, max: list[1].value, rang: list[2].value
        }, balise)
    });
    return list
}

function get_confType() {
    let inputdata = document.getElementById('typeconf');
    let data_type_config = JSON.parse(inputdata.value);
    let type_config = {};
    for (let i = 0; i < data_type_config.length; i++) {
        let conf = JSON.parse(data_type_config[i]);
        type_config[Object.keys(conf)] = conf[Object.keys(conf)];
    }

    return type_config;
}

function save() {
    let data = {};
    let inputnameConf = document.getElementById('nameConf');
    let nameConf = inputnameConf.value;
    let divConf = document.querySelector('.createConfigFile');
    let divMode = divConf.querySelectorAll('.mode');
    for (let i = 0; i < divMode.length; i++) {
        let Tc = divMode[i].querySelectorAll('.testcase');
        let listTc = [];
        for (let j = 0; j < Tc.length; j++) {
            let confTc = Tc[j].querySelectorAll('#configurationTc');
            let dictconf = {};
            for (let k = 0; k < confTc.length; k++) {
                let input = confTc[k].querySelector('.conf');
                if (field.indexOf(input.id) === -1) {
                    if (input.value === "") {
                        dictconf[input.id] = [];
                    } else {
                        dictconf[input.id] = input.value.split(',').map(parseFloat);
                        console.log(input.value.split(',').map(parseFloat));
                    }
                } else if (input.id === 'radio_configuration') {
                    dictconf[input.id] = input.value.split(',');
                } else if (input.id === 'name') {
                    dictconf[input.id] = input.value;
                } else {
                    dictconf[input.id] = Number(input.value);
                }
            }
            listTc.push(dictconf);
        }
        data[divMode[i].id] = listTc;
    }
    console.log(data);
    let file = JSON.stringify(data);
    $.ajax({
        url: '/conf/save',
        data: {data: file, conf: nameConf},
        dataType: 'json',
        Type: 'GET',
        success: function () {
            alert("configuration " + nameConf + " ajouté à la database");
            document.location.href = "../../conf/";
        },
        error: function () {
            alert("ERROR ajax");
        }
    })
}

function addTc(mode) {

    let query = "#" + mode + ".mode";
    let divMode = document.querySelector(query);
    let tc = createTc(mode);
    divMode.appendChild(tc);
}

function rmTc(mode) {

    let query = "#" + mode + ".mode";
    let divMode = document.querySelector(query);
    let listTc = divMode.getElementsByClassName('testcase');
    let rmTc = listTc[listTc.length - 1];
    if (listTc.length !== 0) {
        divMode.removeChild(rmTc);
    }
}

function createTc(mode) {
    let type_config = get_confType();
    let field = ['bbFreq2', 'bbFreq1', 'bbFreqCal', 'inputAttCal', 'inputAtt', 'refLvl', 'rbw', 'vbw',
        'span', 'countAverage', 'pwmeter', 'searchLimit', 'name', 'radio_configuration'];
    let divTc = document.createElement('div');

    divTc.setAttribute('class', 'testcase');

    for (let name_conf in type_config[mode]) {
        let element = document.createElement('input');
        let nameConfElement = document.createElement('p');

        element.name = name_conf;
        element.value = type_config[mode][name_conf];
        element.id = name_conf;
        element.setAttribute('class', 'conf');
        nameConfElement.style.fontWeight = "900";
        nameConfElement.id = "configurationTc";
        nameConfElement.setAttribute('class', 'h3');

        nameConfElement.appendChild(document.createTextNode(element.id + ":"));
        nameConfElement.appendChild(element);

        // create the min max pas
        if (field.indexOf(element.name) === -1) {
            let list = createRange(element);

            for (let i = 0; i < list.length - 1; i++) {
                nameConfElement.appendChild(document.createTextNode(list[i].id));
                nameConfElement.appendChild(list[i]);
            }
            nameConfElement.appendChild(list[list.length - 1]);
        }
        divTc.appendChild(nameConfElement);
    }
    return divTc
}

function createMode(mode) {

    let divMode = document.createElement('div');
    let labelMode = document.createElement('label');
    let button_addTc = document.createElement('button');
    let button_rmTc = document.createElement('button');

    divMode.setAttribute('class', 'mode');
    divMode.id = mode;

    labelMode.setAttribute('class','col');
    labelMode.innerText = mode;
    divMode.appendChild(labelMode);

    button_rmTc.setAttribute('class', 'col btn btn-info btn-lg');
    button_addTc.setAttribute('class', 'col btn btn-info btn-lg');
    button_addTc.id = 'button';
    button_addTc.innerText = 'add a carac';
    button_addTc.addEventListener("click", function a() {
        addTc(mode)
    });
    button_rmTc.id = 'button';
    button_rmTc.innerText = 'rm a carac';
    button_rmTc.addEventListener("click", function r() {
        rmTc(mode)
    });

    divMode.appendChild(button_addTc);
    divMode.appendChild(button_rmTc);

    return divMode;
}


// fonction en cours de développement ---> select sur la configuration radio <--------
// function radioConf(){
//
//
//     let selectRadio = document.createElement("select");
//     selectRadio.id = "selectRadio";
//
//     for(let option in radioMode){
//         let radioOption = document.createElement('option');
//         radioOption.text = radioMode[option];
//         radioOption.value =  radioMode[option];
//         selectRadio.add(radioOption);
//     }
//     selectRadio.addEventListener("click",function (){addRadioConf(selectRadio.value)});
//
//     $('#radio_configuration').parent().append(selectRadio);
//
//
// }
//
// function addRadioConf(value) {
//     let inputRadioConfig = document.getElementById("radio_configuration");
//     inputRadioConfig.disabled = true;
//     let text = inputRadioConfig.value;
//     text = text + "," + value;
//     inputRadioConfig.value = text;
// }
//////////////


var Module = (function(){

    this.save = save();
    this.addTc = addTc(mode);
    this.rmTc = rmTc(mode);
});




let divCreateConfFile = document.querySelector('.createConfigFile');
let configType = get_confType();

for (let mode in configType) {
    console.log(mode);
    let divMode = createMode(mode);
    divCreateConfFile.appendChild(divMode);
}



