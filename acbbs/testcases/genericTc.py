# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

class genericTc(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)

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
                        self.__writeMeasure({"temperature":temperature, "vdd":vdd, "power":power, "dutID":dutID},
                                            {"preamp0":"LNA", "preamp1":"ATTEN", "preamp2":"LNA", "irr":12})

        #write measures in database
        self.db.writeDataBase(self.__createDocument())

    def __writeMeasure(self, dataIn, dataOut):
        self.allMeasures.append({
            "data-input":{
                "dutID":dataIn["dutID"],
                "temperature":dataIn["temperature"],
                "vdd":dataIn["vdd"],
                "power":dataIn["power"]
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
                "preamp0":dataOut["preamp0"],
                "preamp1":dataOut["preamp1"],
                "preamp2":dataOut["preamp2"],
                "irr":dataOut["irr"]
            }
        })

    def __createDocument(self):
        return {
            "date":self.date,
            "bench_informations":{
                "tc_version":"1.0.0",
                "acbbs_version":"1.0.0"
            },
            "tcConfiguration":{
                "temperature":self.tcConf["temperature"],
                "voltage":self.tcConf["voltage"],
                "power":self.tcConf["power"]
            },
            "measures":self.allMeasures
        }
