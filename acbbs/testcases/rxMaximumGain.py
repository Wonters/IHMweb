# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.Swtch import *

class rxMaximumGain(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #store var
        self.temp = temp
        self.simulate = simulate

        #calcul iterations number
        bbIter = 0
        for i in range(self.tcConf["bbFreqLow"], self.tcConf["bbFreqHigh"] + 1, self.tcConf["bbFreqStep"]):
            bbIter += 1
        self.iterationsNumber = len(self.tcConf["channel"]) * len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * len(self.tcConf["freq"]) * bbIter
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.tcConf["channel"]:
            if self.status is st().ABORTING:
                break
            RFSigGenOffset = self.Swtch.setSwitch(sw1 = chan) #configure Swtch channel
            self.DCPwr.setChan(dutChan = chan)         #configure DCPwr channel
            self.dut = dut(chan=chan, simulate=self.simulate) #dut drivers init

            #configuration dut
            self.dut.mode = "RX"
            self.dut.preamp0 = self.tcConf["backoff"][1]
            self.dut.preamp1 = self.tcConf["backoff"][2]
            self.dut.preamp2 = self.tcConf["backoff"][3]

            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for power in self.tcConf["power"]:
                    if self.status is st().ABORTING:
                        break
                    self.RFSigGen.power = power + RFSigGenOffset["smb100a"] #configure power


                    for freq in self.tcConf["freq"]:
                        if self.status is st().ABORTING:
                            break
                        self.dut.freqRx = freq         #configure dut freq

                        for dfreq in range(self.tcConf["bbFreqLow"], self.tcConf["bbFreqHigh"] + 1, self.tcConf["bbFreqStep"]):
                            if self.status is st().ABORTING:
                                break

                            #update progress
                            self.iteration += 1
                            self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))

                            #set SigGen freq
                            self.RFSigGen.freq = freq + dfreq

                            #start measurement
                            rssi = self.dut.rssiSin(freqBBHz = dfreq)

                            #write measures
                            conf = {
                                "vdd":vdd,
                                "power":power,
                                "freq":freq,
                                "temp":self.temp,
                                "baseband":dfreq,
                                "backoff":self.tcConf["backoff"][0],
                                "preamp0":self.tcConf["backoff"][1],
                                "preamp1":self.tcConf["backoff"][2],
                                "preamp2":self.tcConf["backoff"][3]
                            }
                            result = {
                                "rssi":rssi,
                                "gain":float(rssi) - float(power)
                            }
                            self.db.writeDataBase(self.__writeMeasure(conf, result))

                            if self.simulate:
                                time.sleep(0.2)

        #update status
        self.status = st().FINISHED

    def tcInit(self):
        #update status
        self.status = st().INIT

        #ate drivers init
        self.logger.info("Init ate")
        self.DCPwr = DCPwr(simulate=self.simulate)
        self.RFSigGen = RFSigGen(simulate=self.simulate)
        self.Swtch = Swtch(simulate=self.simulate)

        #ate configuration
        self.Swtch.setSwitch(sw2 = 4, sw3 = 3, sw4 = 1)
        self.RFSigGen.power = -130
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
