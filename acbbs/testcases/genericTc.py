# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.Swtch import *

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

        #update Status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for dutID in ['CAFE', 'BABE', 'R2D2', 'Z6PO']:
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

    def tcInit(self):
        #update Status
        self.status = st().INIT

        #init script
        self.logger.info("Init \"{0}\"".format(self.__class__.__name__))

        #ate drivers init
        self.ClimCham = ClimCham()
        self.DCPwr = DCPwr()
        self.PwrMeter = PwrMeter()
        self.RFSigGen = RFSigGen()
        self.SpecAn = SpecAn()
        self.Swtch = Swtch()

        #dut drivers init
        self.dut = dut()

    def __writeMeasure(self, conf, result):
        return {
            "dut-id":conf["dutID"],
            "date-measure":time.time(),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":self.conf.getVersion(),
            "status":self.status,
            "input-parameters":{
                "temperature":conf["temperature"],
                "vdd":conf["vdd"],
                "power":conf["power"]
            },
            "dut-allMeasure":self.dut.allMeasure(),
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
                "PwrMeter":{
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
                },
                "SpecAn":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":["57", "64"],
                    "status":"ERROR",
                    "power":"-90",
                    "frequence":"869525000"
                },
                "Swtch":{
                    "reference":"xxxxxxxxx",
                    "version":"xxxxxxxxx",
                    "error":["57", "64"],
                    "input":"2",
                    "output":"1"
                }
            },
            "dut-result":{
                "i9":result["i9"],
                "i12":result["i12"],
                "pout":result["pout"]
            }
        }
