function createRange(balise) {
    var pas = document.createElement('input');
    var min = document.createElement('input');
    var max = document.createElement('input');
    pas.id = "pas";
    min.id = "min";
    max.id = "max";
    pas.class = 'input1';
    min.class = 'input1';
    max.class = 'input1';
    pas.type = 'range';
    min.type = 'number';
    max.type = 'number';
    var val_pas = document.createTextNode(pas.value);
    val_pas.id = '';
    var list = [min, max, pas, val_pas];
    for (var i = 0; i < list.length; i++) {
        balise.appendChild(document.createTextNode(list[i].id));
        balise.appendChild(list[i]);
    }
    pas.addEventListener('change', function () {
        val_pas.innerHTML = pas.value;
    });

}

var field = ['bbFreq2', 'bbFreq1', 'bbFreqCal', 'inputAttCal', 'inputAtt', 'refLvl', 'rbw', 'vbw',
    'span', 'countAverage', 'pwmeter', 'searchLimit', 'name', 'radio_configuration'];

var balisetest = document.querySelector('.test');

var inputdata = document.getElementById('data');
var config_json = JSON.parse(inputdata.value);
var inputhidden = document.getElementById('info');
var info = JSON.stringify(eval('(' + inputhidden.value + ')'));
info = JSON.parse(info);

for (var mode in config_json) {
    balisetest.appendChild(document.createTextNode(mode));
    for (var tc_num in config_json[mode]) {
        balisetest.appendChild(document.createTextNode(tc_num));
        for (var name_conf in config_json[mode][tc_num]) {
            var element = document.createElement('input');
            var baliseElement = document.createElement('p');
            element.name = name_conf;
            element.value = config_json[mode][tc_num][name_conf];
            element.id = name_conf;
            baliseElement.style.fontWeight = "900";
            baliseElement.appendChild(document.createTextNode(element.id + ":"));
            baliseElement.appendChild(element);
            if (field.indexOf(element.name) === -1) {
                createRange(baliseElement);
            }
            balisetest.appendChild(baliseElement);
        }
    }
}
