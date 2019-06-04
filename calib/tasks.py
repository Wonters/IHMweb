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

from .drivers.PwrMeterCal import PowerMeterCal
from .drivers.RFSigGenCal import RFSigGenCal

import configuration

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

CHANNELS = configuration.CHANNELS
INPUTS = configuration.INPUTS

CONF_PATH = configuration.CONF_PATH

LIST_PATH = configuration.LIST_PATH

class NetworkEquipment(object):
    def __init__(self, simu):
        logger.info('class Ping init')
        self.PwrMeter = PwrMeter(simulate=simu)
        self.SpecAn = SpecAn(simulate=simu)
        self.RFSigGen = RFSigGen(simulate=simu)
        self.RFSigGenV = RFSigGenV(simulate=simu)
        self.Swtch = Swtch(simulate=simu)
        self.ClimCham = ClimCham(simulate=simu)
        self.DCPwr = DCPwr(simulate=simu)
        self.PwrMeterCal = PowerMeterCal(simulate=simu)
        self.RFSigGenCal = RFSigGenCal(simulate=simu)

        self.get_ip()

    def get_ip(self):
        ip_specAn = self.SpecAn.SpecAnConf['ip']
        ip_sigGen = self.RFSigGen.sigGenConf['ip']
        ip_pwMeter = self.PwrMeter.PwrMeterConf['ip']
        ip_sigGenV = self.RFSigGenV.sigGenConf['ip']
        ip_ClimCham = self.ClimCham.dcConf['ip']
        ip_dc1 = self.DCPwr.dcConf['powerDevice1-ip']
        ip_dc2 = self.DCPwr.dcConf['powerDevice2-ip']

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
        global result
        for mode, instrums in self.listIP.items():
            if instrum in instrums.keys():
                result = self.ping_one(self.listIP[mode][instrum])
                break
        return result

    def check_all_instruments(self):
        listPing = self.ping_all()
        if all(i == 0 for i in listPing):
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


class Calibration(object):
    def __init__(self, tab_freq, pwr, simu):
        self.equipement = NetworkEquipment(simu=simu)
        self.tab_freq = tab_freq
        self.OUTPUT_POWER_CALIBRATION = int(pwr)
        self.channels = CHANNELS
        self.simu = simu

        self.paths = LIST_PATH

        self.matSwtchLoss = MatrixCal(CONF_PATH)

        self.loss = {"J5": {}, "J4": {}, "J4_20dB": {}, "J2": {}, "J3": {}, "J18": {}}
        self.delta = {}

        self.pathlist = list()
        for i in self.paths.keys():
            self.pathlist.append(i)

    def calibrate(self):

        # checkPwrMeter = self.equipement.check_one_instrument("PwrMeter")
        # checkRFSigGen = self.equipement.check_one_instrument("RFSigGen")

        # if checkPwrMeter == 0 and checkRFSigGen == 0:
        #    print('Instruments are connected')

        print('calibration')
        self.SMBCal()
        self.SMBVCal()
        self.PwrMeterCal()
        self.FSWCal()
        self.NoiseCal()

        self.makeDelta()
        self.makeMatrixCal()
        print(self.loss)


    def SMBCal(self):
        loss = {"J4": {}, "J4_20dB": {}}

        pathJ4Jx = self.pathlist[1]

        # calibration of J4_20dB - J9
        print(" calibration of SMB -20dB, plug the power meter cal to J9")
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ4Jx]["sw3"], sw4=self.paths[pathJ4Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.RFSigGen.freq = freq
            self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
            # self.equipement.PowerMeterCal = freq
            self.equipement.RFSigGen.status = 1
            time.sleep(1)
            loss["J4_20dB"][freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeterCal.power(nbr_mes=1)
            self.equipement.RFSigGen.status = 0
        self.loss["J4_20dB"]["J9"] = loss["J4_20dB"]

        print(" calibration of SMB, plug the power meter of the cal to J9 to start")
        # calibration of J4 - Jx
        for channel in self.channels:
            print(" plug the power meter cal to J{0}".format(channel + 8))
            port = pathJ4Jx.replace("Jx", "J" + str(channel + 8))
            self.equipement.Swtch.setSwitch(sw1=channel, sw3=self.paths[pathJ4Jx]["sw3"],
                                            sw4=self.paths[pathJ4Jx]["sw4"])
            for freq in self.tab_freq:
                self.equipement.RFSigGen.freq = freq
                self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
                # self.equipement.PowerMeterCal = freq
                self.equipement.RFSigGen.status = 1
                time.sleep(1)
                loss["J4"][freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeterCal.power(nbr_mes=1)
                self.equipement.RFSigGen.status = 0
            self.loss["J4"]["J" + str(channel + 8)] = loss["J4"]

    def SMBVCal(self):
        loss = {"J3": {}}

        pathJ3Jx = self.pathlist[3]

        print(" calibration of SMBV, plug the power meter of the cal to J9")
        # calibration of J3 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ3Jx]["sw3"], sw4=self.paths[pathJ3Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.RFSigGenV.freq = freq
            self.equipement.RFSigGenV.power = self.OUTPUT_POWER_CALIBRATION
            # self.equipement.PowerMeterCal = freq
            self.equipement.RFSigGenV.status = 1
            time.sleep(1)
            loss["J3"][freq] = self.OUTPUT_POWER_CALIBRATION  - self.equipement.PwrMeterCal.power(nbr_mes=1)
            self.equipement.RFSigGenV.status = 0
        self.loss["J3"]["J9"] = loss["J3"]

    def PwrMeterCal(self):
        loss = {"J2": {}}

        pathJ2Jx = self.pathlist[5]

        print(" calibration of Power Meter, plug the RF generator cal to J9")
        # calibration of J2 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ2Jx]["sw3"], sw4=self.paths[pathJ2Jx]["sw4"])
        for freq in self.tab_freq:
            # self.equipement.RFSigGenCal.freq = freq
            # self.equipement.RFSigGenCal.power = self.OUTPUT_POWER_CALIBRATION
            self.equipement.PwrMeter.freq = freq
            time.sleep(1)
            loss["J2"][freq] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeter.power
            # self.equipement.RFSigGenCal.status = 0
        self.loss["J2"]["J9"] = loss["J2"]

    def FSWCal(self):
        loss = {"J5": {}}

        pathJ2Jx = self.pathlist[4]
        print(" calibration of FSW, plug the RF generator cal to J9")
        # calibration of J5 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ2Jx]["sw3"], sw4=self.paths[pathJ2Jx]["sw4"])
        for freq in self.tab_freq:
            # self.equipement.RFSigGenCal.freq = freq
            # self.equipement.RFSigGenCal.power = self.OUTPUT_POWER_CALIBRATION
            # self.equipement.RFSigGenCal.status = 1
            self.equipement.SpecAn.freqSpan = 10000000
            pic = self.equipement.SpecAn.markerPeakSearch()
            time.sleep(1)
            loss["J5"][freq] = self.OUTPUT_POWER_CALIBRATION - pic[1]
            # self.equipement.RFSigGenCal.status = 0
        self.loss["J5"]["J9"] = loss["J5"]

    ######### NON CODE ################
    def NoiseCal(self):
        loss = {"J18":{}}

        pathJ18Jx = self.pathlist[0]
        print(" calibration of Noise, plug the RF generator cal to J18 and the power meter to J9")
        # calibration of J5 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ18Jx]["sw3"], sw4=self.paths[pathJ18Jx]["sw4"])
        for freq in self.tab_freq:
            loss["J18"][freq] = self.OUTPUT_POWER_CALIBRATION
        self.loss["J18"]["J9"] = loss["J18"]

    def makeDelta(self):
        for channel in self.channels:
            Jout = "J" + str(channel + 8)
            delta_freq = {}
            self.delta[Jout]= {}
            for freq in self.tab_freq:
                delta_freq[freq] = self.loss["J4"][Jout][freq] - self.loss["J4"]["J9"][freq]
            self.delta[Jout]= delta_freq

    def makeMatrixCal(self):
        for Jin in self.loss.keys():
            for channel in self.channels[1:]:
                Jout = "J" + str(channel + 8)
                self.loss[Jin][Jout] = {}
                estimate_loss ={}
                for freq in self.tab_freq:
                     estimate_loss[freq] = self.loss[Jin]["J9"][freq] + self.delta[Jout][freq]
                self.loss[Jin][Jout] = estimate_loss



