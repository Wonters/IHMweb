import os


##### import testcases ####################
from acbbs.testcases.rxExcursion import rxExcursion
from acbbs.testcases.txExcursion import txExcursion
from acbbs.testcases.txIM3Measurement import txIM3Measurement
from acbbs.testcases.txPowVsFreq import txPowVsFreq
from acbbs.testcases.txOLFrequency import txOLFrequency

TESTCASES = {
    "rxExcursion": rxExcursion,
    "txExcursion": txExcursion,
    "txIM3Measurement": txIM3Measurement,
    "txPowVsFreq": txPowVsFreq,
    "txOLFrequency": txOLFrequency,
    ## nouveau testcase ##

}

#### settings pour la base de donnée mongo #############
DATABASE_IP = "127.0.0.1"
DATABASE_PORT = "27017"
DATABASE_NAME = "acbbs-configuration"
DATABASE_NAME_CALIB = "acbbs-calibration"
DATABASE_MAXDELAY = 500




##### fichiers mère de configuration de chaque testcase #######
CONFIGFILES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/rxExcursion.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txExcursion.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txIM3Measurement.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txOLFrequency.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txPowVsFreq.json.json'),

    #.... ajouter les chemins de nouveaux testcase ici
]

#### tableau des channels disponibles ###########
CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8]


#### Ce chemin n'est plus necéssaire, tout les fichiers de calibration sont enregistrer dans la base de donnée ######
CONF_PATH = "/etc/acbbs/swtch_cal.json"

#### Ports en entrée du switch ##############
INPUTS = ["J2", "J3", "J4", "J4_20dB", "J5", "J18"]
OUTPUTS = ["J9", "J10", "J11", "J12", "J13", "J14", "J15", "J16"]


##### settings des chemins du switch matrix ###########
LIST_PATH = {
    "Jx-J18": {
        "port": "J18",
        "min": 0,
        "max": 5,
        "sw3": 2,
        "sw4": 1
    },
    "Jx-J4": {
        "port": "J4",
        "min": 0,
        "max": 5,
        "sw3": 3,
        "sw4": 1
    },
    "Jx-J4_20dB": {
        "port": "J4",
        "min": 30,
        "max": 40,
        "sw3": 4,
        "sw4": 2
    },
    "Jx-J3": {
        "port": "J3",
        "min": 70,
        "max": 80,
        "sw3": 3,
        "sw4": 1
    },
    "Jx-J5": {
        "port": "J5",
        "min": 20,
        "max": 28,
        "sw3": 4,
        "sw4": 1
    },
    "Jx-J2": {
        "port": "J2",
        "min": 5,
        "max": 15,
        "sw3": 2,
        "sw4": 1
    },
}

####### port de connection des instruments ##########
PORT_SMB = {"J4": {}, "J4_20dB": {}}
PORT_SMBV = {"J3": {}}
PORT_FSW = {"J5": {}}
PORT_PowerMeter = {"J2": {}}
PORT_NOISE = {"J18": {}}


