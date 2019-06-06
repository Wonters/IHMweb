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
from acbbs.tools.log import get_logger
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

import configuration
from .drivers.PwrMeterCal import PowerMeterCal
from .drivers.RFSigGenCal import RFSigGenCal

logger = get_logger('calib')

CHANNELS = configuration.CHANNELS
INPUTS = configuration.INPUTS
OUTPUTS = configuration.OUTPUTS

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

    def check_one_instrument(self, instrum):
        global result
        for mode, instrums in self.listIP.items():
            if instrum in instrums.keys():
                result = self.ping_one(self.listIP[mode][instrum])
                break
        return result

    def ping_all(self):
        list_pingReturn = self.listIP
        for mode, instrums in self.listIP.items():
            for instrum, ip in instrums.items():
                list_pingReturn[mode][instrum] = self.ping_one(ip)
        return list_pingReturn

    def check_all_instruments(self):
        listPing = self.ping_all()
        if all(i == 0 for i in listPing):
            return 0
        else:
            return 1  # renvoyer un tableau qui indique quel instrument est disconnected


class database(object):

    def __init__(self):
        self.__openDataBase()

    def __openDataBase(self):
        # get server, port and database from json configuration file
        server = configuration.DATABASE_IP
        port = configuration.DATABASE_PORT
        database = configuration.DATABASE_NAME_CALIB
        maxSevSelDelay = configuration.DATABASE_MAXDELAY

        try:
            # open MongoDB server
            self.client = MongoClient(server, int(port), serverSelectionTimeoutMS=maxSevSelDelay)

            # check if connection is well
            self.client.server_info()
        except ServerSelectionTimeoutError as err:
            print("{0}".format(err))
            exit(0)

        # open MongoDB database
        self.db = self.client[database]

    def get_available_collection(self):
        return self.db.list_collection_names()

    def get_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
        return self.db[collection].find({})

    def writeDataBase(self, document, collection):
        if collection in self.get_available_collection():
            print("Error: conf {0} exist. You can delete it with --delete {0}".format(collection))

        self.db_collection = self.db[collection]
        try:
            self.db_collection.insert_one(document).inserted_id
        except DuplicateKeyError as err:
            print("{0}".format(err))

    def delete_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
        self.db.drop_collection(collection)


class MatrixCal(object):
    def __init__(self):
        self.calibFile = {"date": "", "loss": {}}
        self.db = database()

    def get_cal(self, date):
        for doc in self.db.get_collection(date):
            calibFile = doc
        return calibFile

    def getlossPath(self, port_in, port_out, date):
        cal = self.get_cal(date)
        data = cal[port_in][port_out]
        return data

    def write_cal(self, data):
        self.calibFile["loss"] = data
        self.calibFile["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.db.writeDataBase(self.calibFile["loss"], self.calibFile["date"])

    def readPath_loss(self, port_in, port_out):
        return self.data["loss"][port_in][port_out]

    def del_cal(self, cal_name):
        self.db.delete_collection(cal_name)

    def history(self):
        return self.db.get_available_collection()


class Calibration(object):
    def __init__(self, simu):
        self.equipement = NetworkEquipment(simu=simu)
        self.channels = CHANNELS
        self.simu = simu

        self.iteration = 0
        self.totalProgress = 0

        self.paths = LIST_PATH

        self.message = ""
        self.response = 0

        self.matrixCal = MatrixCal()

        self.loss = {INPUTS[4]: {}, INPUTS[2]: {}, INPUTS[3]: {}, INPUTS[0]: {}, INPUTS[1]: {}, INPUTS[5]: {}}
        self.delta = {}

        self.pathlist = list()
        for i in self.paths.keys():
            self.pathlist.append(i)

    def calibrate(self, tab_freq, pwr):
        self.tab_freq = tab_freq
        self.OUTPUT_POWER_CALIBRATION = int(pwr)

        self.totalProgress = (len(INPUTS) - 2 + len(OUTPUTS)) * len(tab_freq)

        print('calibration start')
        self.SMBCal()
        self.SMBVCal()
        self.PwrMeterCal()
        self.FSWCal()
        self.NoiseCal()

        self.makeDelta()
        self.makeMatrixCal()

        self.matrixCal.write_cal(self.loss)

    def SMBCal(self):
        loss = configuration.PORT_SMB
        pathJ4Jx = self.pathlist[1]

        # calibration of J4_20dB - J9
        print("calibration of SMB, plug the power meter cal to J9")
        while self.response == 0:
            self.message = " calibration of SMB, plug the power meter cal to J9 "
            time.sleep(0.8)
            print('wait')
        self.message = ""
        self.response = 0

        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ4Jx]["sw3"], sw4=self.paths[pathJ4Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.RFSigGen.freq = freq
            self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
            self.equipement.RFSigGen.status = 1
            time.sleep(1)
            loss["J4_20dB"][str(freq)] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeterCal.power(nbr_mes=1)
            self.equipement.RFSigGen.status = 0
            self.iteration += 1
        self.loss["J4_20dB"]["J9"] = loss["J4_20dB"]

        # calibration of J4 - Jx
        for channel in self.channels:
            print(" plug the power meter cal to J{0}".format(channel + 8))

            while self.response == 0:
                self.message = " plug the power meter cal to {0}".format(channel + 8)
                time.sleep(0.8)
                print('wait')
            self.message = ""
            self.response = 0

            port = pathJ4Jx.replace("Jx", "J" + str(channel + 8))
            self.equipement.Swtch.setSwitch(sw1=channel, sw3=self.paths[pathJ4Jx]["sw3"],sw4=self.paths[pathJ4Jx]["sw4"])

            for freq in self.tab_freq:
                self.equipement.RFSigGen.freq = freq
                self.equipement.RFSigGen.power = self.OUTPUT_POWER_CALIBRATION
                self.equipement.RFSigGen.status = 1
                time.sleep(1)
                loss["J4"][str(freq)] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeterCal.power(nbr_mes=1)
                self.equipement.RFSigGen.status = 0
                self.iteration += 1
            self.loss["J4"]["J" + str(channel + 8)] = loss["J4"]

    def SMBVCal(self):
        loss = configuration.PORT_SMBV
        pathJ3Jx = self.pathlist[3]

        print(" calibration of SMBV, plug the power meter of the cal to J9")

        while self.response == 0:
            self.message = "plug the power meter cal to J9 "
            time.sleep(0.8)
            print('wait')
        self.message = ""
        self.response = 0

        # calibration of J3 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ3Jx]["sw3"], sw4=self.paths[pathJ3Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.RFSigGenV.freq = freq
            self.equipement.RFSigGenV.power = self.OUTPUT_POWER_CALIBRATION
            # self.equipement.PowerMeterCal = freq
            self.equipement.RFSigGenV.status = 1
            time.sleep(1)
            loss["J3"][str(freq)] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeterCal.power(nbr_mes=1)
            self.equipement.RFSigGenV.status = 0
            self.iteration += 1
        self.loss["J3"]["J9"] = loss["J3"]

    def PwrMeterCal(self):
        loss = configuration.PORT_PowerMeter
        pathJ2Jx = self.pathlist[5]

        print(" calibration of Power Meter, plug the RF generator cal to J9")

        while self.response == 0:
            self.message = "plug the RF generator cal to J9"
            time.sleep(0.8)
            print('wait')
        self.message = ""
        self.response = 0

        # calibration of J2 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ2Jx]["sw3"], sw4=self.paths[pathJ2Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.PwrMeter.freq = freq
            time.sleep(1)
            loss["J2"][str(freq)] = self.OUTPUT_POWER_CALIBRATION - self.equipement.PwrMeter.power
            self.iteration += 1
        self.loss["J2"]["J9"] = loss["J2"]

    def FSWCal(self):
        loss = configuration.PORT_FSW
        pathJ2Jx = self.pathlist[4]

        print(" calibration of FSW, plug the RF generator cal to J9")

        while self.response == 0:
            self.message = "plug the RF generator cal to J9"
            time.sleep(0.8)
            print('wait')
        self.message = ""
        self.response = 0

        # calibration of J5 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ2Jx]["sw3"], sw4=self.paths[pathJ2Jx]["sw4"])
        for freq in self.tab_freq:
            self.equipement.SpecAn.freqSpan = 10000000
            pic = self.equipement.SpecAn.markerPeakSearch()
            time.sleep(1)
            loss["J5"][str(freq)] = self.OUTPUT_POWER_CALIBRATION - pic[1]
            self.iteration += 1
        self.loss["J5"]["J9"] = loss["J5"]

    ######### NON CODE ################
    def NoiseCal(self):
        loss = configuration.PORT_NOISE
        pathJ18Jx = self.pathlist[0]
        print(" calibration of Noise, plug the RF generator cal to J18 and the power meter to J9")

        while self.response == 0:
            self.message = "plug the RF generator cal to J18 and the power meter to J9"
            time.sleep(0.8)
            print('wait')
        self.message = ""
        self.response = 0

        # calibration of J5 - J9
        self.equipement.Swtch.setSwitch(sw1=1, sw3=self.paths[pathJ18Jx]["sw3"], sw4=self.paths[pathJ18Jx]["sw4"])
        for freq in self.tab_freq:
            loss["J18"][str(freq)] = self.OUTPUT_POWER_CALIBRATION
            self.iteration += 1
        self.loss["J18"]["J9"] = loss["J18"]

    def makeDelta(self):
        for channel in self.channels:
            Jout = "J" + str(channel + 8)
            delta_freq = {}
            self.delta[Jout] = {}
            for freq in self.tab_freq:
                delta_freq[str(freq)] = self.loss["J4"][Jout][str(freq)] - self.loss["J4"]["J9"][str(freq)]
            self.delta[Jout] = delta_freq

    def makeMatrixCal(self):
        for Jin in self.loss.keys():
            for channel in self.channels[1:]:
                Jout = "J" + str(channel + 8)
                self.loss[Jin][Jout] = {}
                estimate_loss = {}
                for freq in self.tab_freq:
                    estimate_loss[str(freq)] = self.loss[Jin]["J9"][str(freq)] + self.delta[Jout][str(freq)]
                self.loss[Jin][Jout] = estimate_loss
