# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

class genericTc(baseTestCase):
    def __init__(self):
        #legacy
        baseTestCase.__init__(self)

        #create key
        self.measuresKey = {}

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
                        self.__writeMeasure(dutID, "LNA", "ATTEN", "LNA", 456, 12, 12)

            #write measures in database
            self.db.writeDataBase(dutID, self.__createMasterKey())

    def __writeMeasure(self, dutID, preamp0, preamp1, preamp2, baseband, irr, dPhase):
        pass

    def __createMasterKey(self):
        return {
            self.date:{
                "bench_informations":{
                    "{0}_version".format(self.__class__.__name__):"1.0.0",
                    "acbbs_version":"1.0.0"
                },
                "tcConfiguration":{
                    "temperature":self.tcConf["temperature"],
                    "voltage":self.tcConf["voltage"],
                    "power":self.tcConf["power"]
                },
                "measures":self.measuresKey
            }
        }
