import json
import os
import sys
import time

from acbbs.drivers.ate.PwrMeter import PwrMeter
from acbbs.drivers.ate.RFSigGen import RFSigGen
from acbbs.drivers.ate.RFSigGenV import RFSigGenV
from acbbs.drivers.ate.SpecAn import SpecAn
from acbbs.drivers.ate.Swtch import Swtch
from acbbs.tools.configurationFile import configurationFile

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.

# avec ICMP, il est obligatioire de lancer le script en étant superutilisteur root
# Pour piger avec des sockets sans être administrateur il faut compter sur des sockets AF_INET SOCK_STREAM

CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8]

CONF_PATH = "/etc/acbbs/swtch_cal.json"

LIST_PATH = {
    "Jx-J18": {
        "port": "J18",
        "min": 0,
        "max": 5,
        "sw3": 2,
        "sw4": 1
    }
}

LIST_RX = {
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
}

LIST_TX = {
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


class Ping(object):
    def __init__(self):
        print('class Ping init')

    def ping_one(self, IP):
        response = os.system("ping -c 1 " + IP)
        if response == 0:
            print("Network Equipement Active")
            return 1
        else:
            print('Network Equipement Error : {0}'.format(IP))
            return 0

    def ping_all(self, IP_tab):
        list_pingReturn = []
        for key, value in IP_tab.items():
            list_pingReturn.append(self.ping_one(value))
        return list_pingReturn


class read_write(object):
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as json_file:
            self.data = json.load(json_file)

    def write_date(self):
        self.data["calibration-date"] = time.strftime("%Y-%m-%d %H:%M:%S")

    def read_date(self):
        return self.data["calibration-date"]

    def write_cal(self, path, value):
        self.data["loss"][path] = value

    def read_cal(self, path):
        return self.data["loss"][path]

    def __del__(self):
        with open(self.file, "w") as json_file:
            json.dump(self.data, json_file, indent=2, sort_keys=True)


class Calibration(object):
    def __init__(self, parent, freq, pwr, channels, simu, conf):
        print('initialisation calibration')
        self.PwMeter = PwrMeter(simulate=simu)
        self.SpecAn = SpecAn(simulate=simu)
        self.RFSigGen = RFSigGen(simulate=simu)
        self.RFSigGenV = RFSigGenV(simulate=simu)
        self.Swtch = Swtch(simulate=simu)
        self.PwMeter = PwrMeter(simulate=simu)
        self.channels = CHANNELS
        self.get_ip()
        self.ping = Ping()
        self.freq = freq
        self.pwr = pwr
        self.channels = channels
        self.simu = simu
        self.conf = conf

    def get_ip(self):
        self.conf = configurationFile(file=self.SpecAn.__class__.__name__)
        self.specAnConf = self.conf.getConfiguration()
        ip_specAn = self.specAn['ip']

        self.conf = configurationFile(file=self.RFSigGen.__class__.__name__)
        self.sigGenConf = self.conf.getConfiguration()
        ip_sigGen = self.sigGenConf['ip']

        self.conf = configurationFile(file=self.PwMeter.__class__.__name__)
        self.pwMeterConf = self.conf.getConfiguration()
        ip_pwMeter = self.sigGenVConf['ip']

        self.conf = configurationFile(file=self.RFSigGenV.__class__.__name__)
        self.sigGenVConf = self.conf.getConfiguration()
        ip_sigGenV = self.sigGenVConf['ip']

        self.listIP = {'rx': {'RFSingGen': ip_sigGen, 'RFSigGenV': ip_sigGenV},
                       'tx': {'PwMeter': ip_pwMeter, 'SpecAn': ip_specAn}
                       }

    def rxCalibration(self):
        # ping all instuments rx
        ping_list = self.ping.ping_all(self.listIP['rx'])
        if ping_list == True:
            print('bonjour')
        # for i in slef.channels:
        # for instru in générateur;

        print('calibration RX')

    def txCalibration(self):
        ping_list = self.ping.ping_all(self.listIP['tx'])
        if ping_list == True:
            print("tx calibration")
        print('calibration tx')

    def alert(self):
        print('alert')

    def ping(self):
        print('ping')

    def init(self):
        try:
            for i in range(0, len(self.channels)):
                self.channels[i] = int(self.channels[i])
        except:
            print("Error parsing DUT channel")
            exit(0)

        if self.simu:
            SIMULATE = True
        else:
            SIMULATE = False

        rw = read_write(CONF_PATH)

        self.RFSigGen.status = 0
        self.RFSigGen.freq = self.freq
        self.RFSigGen.power = self.pwr

        #self.pwMeterConf.freq =

        print("Previous calibration date : {0}\n".format(rw.read_date()))
