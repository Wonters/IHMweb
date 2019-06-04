
import os

DATABASE_IP = "127.0.0.1"
DATABASE_PORT = "27017"
DATABASE_NAME = "acbbs-configuration"
DATABASE_MAXDELAY = 500

CONFIGFILES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/rxExcursion.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txExcursion.json'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/media/format_testcase/txIM3Measurement.json'),
]

CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8]

INPUTS = ["J2", "J3", "J4", "J4_20dB", "J5", "J18"]

CONF_PATH = "/etc/acbbs/swtch_cal.json"

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
