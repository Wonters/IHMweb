# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.Swtch import *

class rxGainLNAs(baseTestCase):
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
            self.dut = dut(chan=chan, simulate = True)                  #dut drivers init

            #configuration dut
            self.dut.mode = "RX"
            self.dut.preamp0 = self.tcConf["preamp0-ref"]
            self.dut.preamp1 = self.tcConf["preamp1-ref"]
            self.dut.preamp2 = self.tcConf["preamp2-ref"]


            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for power in self.tcConf["power"]:
                    if self.status is st().ABORTING:
                        break
                    self.RFSigGen.power = power        #configure power


                    for freq in self.tcConf["freq"]:
                        if self.status is st().ABORTING:
                            break
                        self.dut.freqRx = freq
                        self.RFSigGen.freq = freq

                        for backoff in self.tcConf["backoff"]:
                            if self.status is st().ABORTING:
                                break

                            #update progress
                            self.iteration += 1

                            #configure DUT

                            #configure ATE
                            self.dut.preamp0 = backoff[1]
                            self.dut.preamp1 = backoff[2]
                            self.dut.preamp2 = backoff[3]

                            #start measurement
                            refLevel = self.dut.rssiSin(freqBBHz = self.tcConf["bbFreq"])

                            #write measures
                            conf = {
                                "vdd":vdd,
                                "power":power,
                                "freq":freq,
                                "backoff":backoff[0],
                                "preamp0":backoff[1],
                                "preamp1":backoff[2],
                                "preamp2":backoff[3]
                            }
                            result = {
                                "refLevel":refLevel
                            }
                            self.db.writeDataBase(self.__writeMeasure(conf, result))

        #update Status
        self.status = st().FINISHED

    def tcInit(self):
        #update Status
        self.status = st().INIT

        #ate drivers init
        self.logger.debug("Init ate")
        self.DCPwr = DCPwr(simulate = True)
        self.RFSigGen = RFSigGen(simulate = True)
        self.Swtch = Swtch(simulate = True)

        #ate configuration
        self.Swtch.setSwitch(sw2 = 4, sw3 = 3, sw4 = 1)
        self.RFSigGen.status = 1

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
                "DCPwr":self.DCPwr.info,
                "RFSigGen":self.RFSigGen.info
            },
            "dut-result":result
        }
