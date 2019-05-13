import json
import os
import sys
import time

from acbbs.drivers.ate.ClimCham import ClimCham
from acbbs.drivers.ate.DCPwr import DCPwr
from acbbs.drivers.ate.PwrMeter import PwrMeter
from acbbs.drivers.ate.RFSigGen import RFSigGen
from acbbs.drivers.ate.RFSigGenV import RFSigGenV
from acbbs.drivers.ate.SpecAn import SpecAn
from acbbs.drivers.ate.Swtch import Swtch
from acbbs.tools.configurationFile import configurationFile
from acbbs.tools.log import get_logger

logger = get_logger('calib')

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
INPUT = [1, 2, 3, 4, 5]

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



class NetworkEquipment(object):
    def __init__(self, simu):
        logger.info('class Ping init')
        self.PwMeter = PwrMeter(simulate=simu)
        self.SpecAn = SpecAn(simulate=simu)
        self.RFSigGen = RFSigGen(simulate=simu)
        self.RFSigGenV = RFSigGenV(simulate=simu)
        self.Swtch = Swtch(simulate=simu)
        self.ClimCham = ClimCham(simulate=simu)
        self.DCPwr = DCPwr(simulate=simu)

        self.get_ip()

    def get_ip(self):
        conf = configurationFile(file=self.SpecAn.__class__.__name__)
        self.specAnConf = conf.getConfiguration()
        ip_specAn = self.specAnConf['ip']

        conf = configurationFile(file=self.RFSigGen.__class__.__name__)
        self.sigGenConf = conf.getConfiguration()
        ip_sigGen = self.sigGenConf['ip']

        conf = configurationFile(file=self.PwMeter.__class__.__name__)
        self.pwMeterConf = conf.getConfiguration()
        ip_pwMeter = self.pwMeterConf['ip']

        conf = configurationFile(file=self.RFSigGenV.__class__.__name__)
        self.sigGenVConf = conf.getConfiguration()
        ip_sigGenV = self.sigGenVConf['ip']

        conf = configurationFile(file=self.ClimCham.__class__.__name__)
        self.ClimChamConf = conf.getConfiguration()
        ip_ClimCham = self.ClimChamConf['ip']

        conf = configurationFile(file=self.DCPwr.__class__.__name__)
        self.DCPwrConf = conf.getConfiguration()
        ip_dc1 = self.DCPwrConf['powerDevice1-ip']
        ip_dc2 = self.DCPwrConf['powerDevice2-ip']

        self.listIP = {'rx': {'RFSigGen': ip_sigGen, 'RFSigGenV': ip_sigGenV},
                       'tx': {'PwrMeter': ip_pwMeter, 'SpecAn': ip_specAn},
                       'DC': {'DC1': ip_dc1, 'DC2': ip_dc2},
                       'Chamber': {'climCham': ip_ClimCham},
                       }

    def ping_one(self, IP):
        response = os.system("ping -c 1 " + IP)
        if response == 0:
            logger.info("Network Equipement Active at adresse:{0}".format(IP))
            return 0
        else:
            logger.error('Network Equipement Error : {0}'.format(IP))
            return 1

    def ping_all(self):
        list_pingReturn = self.listIP
        for mode, instrums in self.listIP.items():
            for instrum, ip in instrums.items():
                list_pingReturn[mode][instrum] = self.ping_one(ip)
        return list_pingReturn

    def check_one_instrument(self, instrum):
        for mode, instrums in self.listIP.items():
            print(instrum, instrums.keys())
            if instrum in instrums.keys():
                result = self.ping_one(self.listIP[mode][instrum])
                break
        return result

    def check_all_instruments(self):
        checkRX = self.ping.ping_all(self.listIP['rx'])
        checkTX = self.ping.ping_all(self.listIP['tx'])
        checkDC = self.ping.ping_all(self.listIP['DC'])
        checkclimCham = self.ping.ping_all(self.listIP['climCham'])
        check = []
        check.append(checkRX)
        check.append(checkTX)
        check.append(checkclimCham)
        check.append(checkDC)
        if all(i == 0 for i in check):
            return 0
        else:
            return 1  # renvoyer un tableau qui indique quel instrument est disconnected


class MatrixCal(object):
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


class SwitchCalibration(NetworkEquipment):
    def __init__(self, tab_freq, pwr, simu):
        print('switch calibration')
        self.equipement = NetworkEquipment(simu=simu)
        self.tab_freq = tab_freq
        self.pwr = pwr
        self.channels = CHANNELS
        self.simu = simu

        self.paths = LIST_PATH

        self.OUTPUT_POWER_CALIBRATION = pwr
        self.matSwtchLoss = MatrixCal(CONF_PATH)

    def calibrate(self):
        lossWire_per_freq = {}
        lossWires = {}
        checkPwrMeter = self.equipement.check_one_instrument("PwrMeter")
        checkRFSigGen = self.equipement.check_one_instrument("RFSigGen")

        if checkPwrMeter == 0 and checkRFSigGen == 0:
            print('Instruments are connected')

        for path, settings in self.paths.items():
            for channel in self.channels:
                for freq in self.tab_freq:
                    path_to_calibrate = path.replace("x", str(channel + 8))
                    self.equipement.RFSigGen.freq = freq
                    self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
                    self.equipement.PwMeter.freq = freq
                    self.equipement.Swtch.setSwitch(sw1=channel, sw3=settings["sw3"], sw4=settings["sw4"])
                    self.equipement.RFSigGen.status = 1
                    time.sleep(1)
                    lossWire_per_freq[freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwMeter.power - self.matSwtchLoss.read_cal(path_to_calibrate)
                    lossWires[path_to_calibrate.split('-')[0]] = lossWire_per_freq
                    self.equipement.RFSigGen.status = 0


class WiresCalibration(object):
    def __init__(self, channels, inputs, tab_freq, pwr, simu):
        print("wires calibration")
        self.equipement = NetworkEquipment(simu=simu)
        self.tab_freq = tab_freq
        self.pwr = pwr
        self.channels = channels
        self.inputs = inputs
        self.simu = simu

        self.paths = LIST_PATH

        self.OUTPUT_POWER_CALIBRATION = pwr

        self.matSwtchLoss = MatrixCal(CONF_PATH)

    def calibrate(self):
        # ping all instuments rx
        lossWire_per_freq = {}
        lossWires = {}
        checkPwrMeter = self.equipement.check_one_instrument("PwrMeter")
        checkRFSigGen = self.equipement.check_one_instrument("RFSigGen")

        port_cal_wrDUT = 'J5'
        port_cal_wrINST = 'J9'
        path_cal = 'Jx-'+ port_cal_wrDUT

        if checkPwrMeter == 0 and checkRFSigGen == 0:
            print('Instruments are connected')

        #### calibrate DUT wires
        print('plug the RFSigGen on J5')
        print('wires calibrates to output channels:')
        for channel in self.channels:
            path_to_calibrate = path_cal.replace("x", str(channel + 8))
            print(path_to_calibrate)
            for freq in self.tab_freq:
                self.equipement.RFSigGen.freq = freq
                self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
                self.equipement.PwMeter.freq = freq
                self.equipement.Swtch.setSwitch(sw1=channel, sw3=self.paths[path_cal]["sw3"], sw4=self.paths[path_cal]["sw4"])
                self.equipement.RFSigGen.status = 1
                time.sleep(1)
                lossWire_per_freq[freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwMeter.power - self.matSwtchLoss.read_cal(path_to_calibrate)
                lossWires[path_cal.split('-')[0]] = lossWire_per_freq
                self.equipement.RFSigGen.status = 0

        ### calibrate INPUT wires inputs = [J2, J3, J4, J4_20dB, J5, J18]
        print('plug the PwrMeter on J9')
        print('wires calibrates to input instruments')
        for path in self.paths:
            port = path.split('-')
            for input in self.inputs:
                if input == port[1]:
                    path_to_calibrate = path.replace("Jx", port_cal_wrINST)
                    print(path_to_calibrate)
                    for freq in self.tab_freq:
                        self.equipement.RFSigGen.freq = freq
                        self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
                        self.equipement.PwMeter.freq = freq
                        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[path]["sw3"], sw4=self.paths[path]["sw4"])
                        self.equipement.RFSigGen.status = 1
                        time.sleep(1)
                        lossWire_per_freq[freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwMeter.power - \
                                    self.matSwtchLoss.read_cal(path_to_calibrate)
                        lossWires[path_to_calibrate.split('-')[1]] = lossWire_per_freq
                        self.equipement.RFSigGen.status = 0
        print(lossWires)

