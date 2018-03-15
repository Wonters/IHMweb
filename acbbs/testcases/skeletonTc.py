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
        self.iterationsNumber = self.conf.getTcIterationsNumber()
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update Status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.tcConf["channel"]:
            if self.status is st().ABORTING:
                break
            self.Swtch.setSwitch(sw1 = chan)           #configure Swtch channel
            self.DCPwr.setChan(dutChan = chan)         #configure DCPwr channel
            self.dut = dut(chan=chan, simulate=True)   #dut drivers init


            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for power in self.tcConf["power"]:
                    if self.status is st().ABORTING:
                        break
                    self.RFSigGen.power = power        #configure power


                    #update progress
                    self.iteration += 1

                    #configure DUT

                    #configure ATE

                    #start measurement

                    #simulation
                    i9 = float(vdd) / (float(random.randrange(9000, 12000))/1000.0)
                    i12 = float(vdd) / (float(random.randrange(5000, 19000))/1000.0)

                    #write measures
                    self.db.writeDataBase(self.__writeMeasure(conf = {"vdd":vdd, "power":power},
                                                            result = {"i9":i9, "i12": i12}))

                    #simulation
                    time.sleep(0.1)

        #update Status
        self.status = st().FINISHED

    def tcInit(self):
        #update Status
        self.status = st().INIT

        #ate drivers init
        self.logger.debug("Init ate")
        self.ClimCham = ClimCham(simulate = True)
        self.DCPwr = DCPwr(simulate = True)
        self.PwrMeter = PwrMeter(simulate = True)
        self.RFSigGen = RFSigGen(simulate = True)
        self.SpecAn = SpecAn(simulate = True)
        self.Swtch = Swtch(simulate = True)
        self.Swtch.setSwitch(sw2 = 4, sw3 = 3, sw4 = 1)

    def __writeMeasure(self, conf, result):
        return {
            "date-measure":time.time(),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":self.conf.getVersion(),
            "status":self.status,
            "input-parameters":conf,
            "dut-info":self.dut.info,
            "ate-result":{
                "ClimCham":self.ClimCham.info,
                "DCPwr":self.DCPwr.info,
                "PwrMeter":self.PwrMeter.info,
                "RFSigGen":self.RFSigGen.info,
                "SpecAn":self.SpecAn.info
            },
            "dut-result":result
        }
