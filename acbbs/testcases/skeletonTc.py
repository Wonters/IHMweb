# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.Swtch import *

class skeletonTc(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, temp, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = 0
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.tcConf["channel"]:
            if self.status is st().ABORTING:
                break
            self.Swtch.setSwitch(sw1 = chan)           #configure Swtch channel
            self.DCPwr.setChan(dutChan = chan)         #configure DCPwr channel
            self.dut = dut(chan=chan, simulate=self.simulate) #dut drivers init

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

                    #write measures
                    conf = {
                        "vdd":vdd,
                        "power":power,
                        "freq":freq,
                        "temp":self.temp
                    }
                    result = {
                    }
                    self.db.writeDataBase(self.__writeMeasure(conf, result))

                    if self.simulate:
                        time.sleep(0.02)

        #update status
        self.status = st().FINISHED

    def tcInit(self):
        #update status
        self.status = st().INIT

        #ate drivers init
        self.logger.debug("Init ate")
        self.DCPwr = DCPwr(simulate=self.simulate)
        self.PwrMeter = PwrMeter(simulate=self.simulate)
        self.RFSigGen = RFSigGen(simulate=self.simulate)
        self.SpecAn = SpecAn(simulate=self.simulate)
        self.Swtch = Swtch(simulate=self.simulate)
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
