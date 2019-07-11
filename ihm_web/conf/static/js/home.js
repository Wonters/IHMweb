function initConf(value) {
    let name_index = '';
    $.ajax({
        url: '/conf/init',
        dataType: 'json',
        type: 'GET',
        data: {configname: value},
        success: function s(data_return) {
            //document.location.href = "../../conf/";
            name_index = data_return['name'];
        },
        error: function e() {
            alert("Error ajax");
        },
    });
    let select = document.getElementById('select');
    for (let index = 0; index < select.options.length; index++) {
        if (select[index].value === name_index) {
            select.selectedIndex = index;
        }

    }
}

function deleteConf() {
    if (confirm("Etes vous sûr de vouloir supprimer la configuration " + document.getElementById('select').value)) {
        // faire un formulaire
        var configName = document.querySelector('#select').value;
        console.log(configName);
        $.ajax(
            {
                url: '/conf/delete',
                dataType: 'json',
                data: {conf: configName},
                Type: 'GET',
            }
        );
        document.location.href = '/conf/';
    }
}

function addConf() {
    var form = document.querySelector('.loadfile');
    if (form.elements.file.files[0].type === "application/json") {
        form.submit();
    } else {
        alert("the file selected is not an available configuration");
    }
}


