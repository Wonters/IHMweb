# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.Swtch import *

#simulation
import random

class rxGainLNA(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * 1 #nb dut

    def run(self):
        #update Status
        self.status = st().STARTING

        #update Status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))

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

                #write measures
                self.db.writeDataBase(self.__writeMeasure(conf = {"vdd":vdd, "power":power},
                                                        result = {}))

        #update Status
        self.status = st().FINISHED

    def tcInit(self):
        #update Status
        self.status = st().INIT

        #init script
        self.logger.info("Init ".format(self.__class__.__name__))

        #ate drivers init
        self.logger.debug("Init ate")
        self.DCPwr = DCPwr(simulate = True)
        self.RFSigGen = RFSigGen(simulate = True)

        self.DCPwr.selChan(1)

        #dut drivers init
        self.logger.debug("Init dut")
        self.dut = dut(simulate = True)

        #get ate version and reference
        self.logger.debug("Get ate references and versions")
        self.DCPwrVer = self.DCPwr.version
        self.RFSigGenRef = self.RFSigGen.reference
        self.RFSigGenVer = self.RFSigGen.version

    def __writeMeasure(self, conf, result):
        return {
            "dut-id":self.dut.tapId,
            "date-measure":time.time(),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":self.conf.getVersion(),
            "status":self.status,
            "input-parameters":{
                "vdd":conf["vdd"],
                "power":conf["power"]
            },
            "dut-allMeasure":self.dut.allMeasure,
            "ate-result":{
                "DCPwr":{
                    "version":self.DCPwrVer,
                    "error":self.DCPwr.errors,
                    "status":self.DCPwr.status,
                    "current_consigne":self.DCPwr.currentConsigne,
                    "current_real":self.DCPwr.currentReal,
                    "voltage_consigne":self.DCPwr.voltageConsigne,
                    "voltage_real":self.DCPwr.voltageReal
                },
                "RFSigGen":{
                    "reference":self.RFSigGenRef,
                    "version":self.RFSigGenVer,
                    "error":self.RFSigGen.errors
                }
            },
            "dut-result":{
            }
        }
