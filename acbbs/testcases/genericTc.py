# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

from os.path import basename, splitext
from time import strftime

class genericTc(baseTestCase):
    def __init__(self):
        #legacy
        baseTestCase.__init__(self)

        #init dataBase
        self.db = dataBase(collection = splitext(basename(__file__))[0])

        #get configuration testcases
        self.conf = configurationFile(file = splitext(basename(__file__))[0])
        self.tcConf = self.conf.getConfiguration()

        #variables
        self.measures = []

    def run(self):
        #start loop
        for dutID in ['CAFE', 'BABE', 'R2D2', 'Z6PO']:
            for temperature in self.tcConf["temperature"]:
                for vdd in self.tcConf["voltage"]:
                    for power in self.tcConf["power"]:

                        #configure DUT

                        #configure ATE

                        #start measurement

                        #write measures
                        self.measures.append(self.__formatMeasures(temperature, vdd, power, "LNA", "ATTEN", "LNA", 456, 12, 12, vdd))

        #write measures in databsae
        self.db.writeDataBase(self.__formatDict(self.measures))

    def __formatDict(self, measure):
        return {
            "bench_informations":{
                "version":"1.0.0",
                "date":strftime("%Y_%m_%d"),
                "heure":strftime("%H_%M_%S")
            },
            "tcConfiguration":{
                "temperature":self.tcConf["temperature"],
                "voltage":self.tcConf["voltage"],
                "power":self.tcConf["power"]
            },
            "measures":measure
        }

    def __formatMeasures(self, temperature, vdd, power, preamp0, preamp1, preamp2, baseband, irr, dPhase, dGain):
        return {
            "data-input":{
                "dut-id":"R2D2",
                "tc-name":"genericTc",
                "temperature":temperature,
                "vdd":vdd,
                "power":power
            },
            "ate-configuration":{
                "ClimCham":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":[],
                    "temp_consigne":"20",
                    "temp_real":"20.02",
                    "humidity_consigne":"80",
                    "humidity_real":"80.2"
                },
                "Swtch":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":["57", "64"],
                    "input":"2",
                    "output":"1"
                },
                "DCPwr":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":["57", "64"],
                    "status":"ON",
                    "current_consigne":"5",
                    "current_real":"2.6",
                    "voltage_consigne":"12.5",
                    "voltage_real":"12.5"
                },
                "RFSigGen":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":["57", "64"],
                    "status":"ERROR",
                    "power":"-90",
                    "frequence":"869525000"
                }
            },
            "data-output":{
                "preamp0":preamp0,
                "preamp1":preamp1,
                "preamp2":preamp2,
                "baseband":baseband,
                "irr":irr,
                "dPhase":dPhase,
                "dGain":dGain
            }
        }
