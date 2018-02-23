# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

from time import strftime

class genericTc(baseTestCase):
    def __init__(self):
        #legacy
        baseTestCase.__init__(self)

        #create master key
        self.__createMasterKey()

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
                        pass

            #write measures in databsae
            self.db.writeDataBase(dutID, self.masterKey)

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

    def __writeMeasure(self, dutID, preamp0, preamp1, preamp2, baseband, irr, dPhase):
        pass

    def __createMasterKey(self):
        self.masterKey = {self.date:""}
