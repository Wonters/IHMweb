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

class skeletonTc(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.tcConf["temperature"]) * len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * len(self.tcConf["dut-ip"])
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update Status
        self.status = st().STARTING

        #update Status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for dutIP in self.tcConf["dut-ip"]:
            #if status = ABORTING, finish iteration and break :
            if self.status is st().ABORTING:
                break

            #dut drivers init
            self.logger.debug("Init dut")
            self.logger.debug("Check dut-ip : {0}".format(dutIP))
            self.dut = dut(dutIP)
            if self.dut.connected:
                self.logger.debug("DUT at {0} well connected".format(dutIP))
            else:
                self.logger.error("dut error, aborting...")
                self.status = st().ABORTING


            for temperature in self.tcConf["temperature"]:
                #if status = ABORTING, finish iteration and break :
                if self.status is st().ABORTING:
                    break


                for vdd in self.tcConf["voltage"]:
                    #if status = ABORTING, finish iteration and break :
                    if self.status is st().ABORTING:
                        break


                    for power in self.tcConf["power"]:
                        #if status = ABORTING, finish iteration and break :
                        if self.status is st().ABORTING:
                            break


                        #update progress
                        self.iteration += 1

                        #configure DUT

                        #configure ATE

                        #start measurement

                        #simulation
                        i9 = float(vdd) / (float(random.randrange(9000, 12000))/1000.0)
                        i12 = float(vdd) / (float(random.randrange(5000, 19000))/1000.0)
                        pout = temperature * random.randrange(7, 9)

                        #write measures
                        self.db.writeDataBase(self.__writeMeasure(conf = {"temperature":temperature, "vdd":vdd, "power":power},
                                                                result = {"i9":i9, "i12": i12, "pout":pout}))

                        #simulation
                        time.sleep(0.1)

        #update Status
        self.status = st().FINISHED

    def tcInit(self):
        #update Status
        self.status = st().INIT

        #init script
        self.logger.info("Init ".format(self.__class__.__name__))

        #ate drivers init
        self.logger.debug("Init ate")
        self.ClimCham = ClimCham()
        self.DCPwr = DCPwr(simulate = True)
        self.DCPwr.selChan(1)
        self.PwrMeter = PwrMeter()
        self.RFSigGen = RFSigGen(simulate = True)
        self.SpecAn = SpecAn()
        self.Swtch = Swtch(simulate = True)

        #get ate version and reference
        self.logger.debug("Get ate references and versions")
        self.ClimChamRef = self.ClimCham.reference
        self.ClimChamVer = self.ClimCham.version
        self.DCPwrVer = self.DCPwr.version
        self.PwrMeterRef = self.PwrMeter.reference
        self.PwrMeterVer = self.PwrMeter.version
        self.RFSigGenRef = self.RFSigGen.reference
        self.RFSigGenVer = self.RFSigGen.version
        self.SpecAnRef = self.SpecAn.reference
        self.SpecAnVer = self.SpecAn.version
        self.SwtchRef = self.Swtch.reference
        self.SwtchVer = self.Swtch.version

    def __writeMeasure(self, conf, result):
        return {
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
            "dut-info":{
                "id":self.dut.tapId,
                "tap-hw":self.dut.tapHw,
                "tap-sw":self.dut.tapSw,
                "radio-hw":self.dut.radioHw,
                "radio-fw":self.dut.radioFw,
                "tpm-hw":self.dut.tpmHw,
                "tpm-vendor":self.dut.tpmVendor,
                "freq-tx":self.dut.freqTx,
                "freq-rx":self.dut.freqRx,
                "mode":self.dut.mode,
                "preamp0":self.dut.preamp0,
                "preamp1":self.dut.preamp1,
                "preamp2":self.dut.preamp2,
                "measure":self.dut.allMeasure
            },
            "ate-result":{
                "ClimCham":{
                    "reference":self.ClimChamRef,
                    "version":self.ClimChamVer,
                    "error":self.ClimCham.errors,
                    "temp_consigne":self.ClimCham.tempConsigne,
                    "temp_real":self.ClimCham.tempReal,
                    "humidity_consigne":self.ClimCham.humidityConsigne,
                    "humidity_real":self.ClimCham.humidityReal
                },
                "DCPwr":{
                    "version":self.DCPwrVer,
                    "error":self.DCPwr.errors,
                    "status":self.DCPwr.status,
                    "current_consigne":self.DCPwr.currentConsigne,
                    "current_real":self.DCPwr.currentReal,
                    "voltage_consigne":self.DCPwr.voltageConsigne,
                    "voltage_real":self.DCPwr.voltageReal
                },
                "PwrMeter":{
                    "reference":self.PwrMeterRef,
                    "version":self.PwrMeterVer,
                    "error":self.PwrMeter.errors
                },
                "RFSigGen":{
                    "reference":self.RFSigGenRef,
                    "version":self.RFSigGenVer,
                    "error":self.RFSigGen.errors
                },
                "SpecAn":{
                    "reference":self.SpecAnRef,
                    "version":self.SpecAnVer,
                    "error":self.SpecAn.errors
                },
                "Swtch":{
                    "reference":self.SwtchRef,
                    "version":self.SwtchVer,
                    "error":self.SpecAn.errors
                }
            },
            "dut-result":{
                "i9":result["i9"],
                "i12":result["i12"],
                "pout":result["pout"]
            }
        }
