# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

import time

#simulation
import random

class genericTc(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.tcConf["temperature"]) * len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * 4 #nb dut

    def run(self):
        #update Status
        self.status = st().STARTING

        #init script
        self.logger.debug("Init \"{0}\"........".format(self.__class__.__name__))

        #simulation
        time.sleep(3)

        #update Status
        self.status = st().RUNNING

        #start loop
        self.logger.debug("Start loop of \"{0}\"........".format(self.__class__.__name__))
        for dutID in ['CAFE', 'BABE', 'R2D2', 'Z6PO', 'DRZ', 'FZAS', 'XXFE', 'TKKO', 'COZUX', 'LEJUXB', 'AKSUF', 'EAHSE']:
            #if status = ABORTING, finish iteration and break :
            if self.status is st().ABORTING:
                continue

            for temperature in self.tcConf["temperature"]:
                #if status = ABORTING, finish iteration and break :
                if self.status is st().ABORTING:
                    continue

                for vdd in self.tcConf["voltage"]:
                    #if status = ABORTING, finish iteration and break :
                    if self.status is st().ABORTING:
                        continue

                    for power in self.tcConf["power"]:
                        #if status = ABORTING, finish iteration and break :
                        if self.status is st().ABORTING:
                            continue

                        #update progress
                        self.progress += 1

                        #configure DUT

                        #configure ATE

                        #start measurement

                        #simulation
                        i9 = float(vdd) / (float(random.randrange(9000, 12000))/1000.0)
                        i12 = float(vdd) / (float(random.randrange(5000, 19000))/1000.0)
                        pout = temperature * random.randrange(7, 9)

                        #write measures
                        self.db.writeDataBase(self.__writeMeasure(conf = {"dutID":dutID, "temperature":temperature, "vdd":vdd, "power":power},
                                                                result = {"i9":i9, "i12": i12, "pout":pout}))

                        #simulation
                        time.sleep(0.1)

        #update Status
        self.status = st().FINISHED

    def __writeMeasure(self, conf, result):
        return {
            "dut-id":conf["dutID"],
            "date-measure":int(strftime("%Y%m%d%H%M%S")),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":self.conf.getVersion(),
            "tcConfiguration":{
                "temperature":self.tcConf["temperature"],
                "voltage":self.tcConf["voltage"],
                "power":self.tcConf["power"]
            },
            "configuration":{
                "status":self.status,
                "temperature":conf["temperature"],
                "vdd":conf["vdd"],
                "power":conf["power"]
            },
            "ate-result":{
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
            "dut-result":{
                "i9":result["i9"],
                "i12":result["i12"],
                "pout":result["pout"]
            }
        }
