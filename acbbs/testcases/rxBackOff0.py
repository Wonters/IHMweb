# coding=UTF-8

from ..testcases.baseTestCase import baseTestCase, st
from ..drivers.ate.DCPwr import DCPwr
from ..drivers.ate.RFSigGen import RFSigGen
from ..drivers.ate.Swtch import Swtch
from ..drivers.ate.ClimCham import ClimCham
from ..drivers.dut import Dut
from .. import __version__
import time

class rxBackOff0(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, temp, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.tcConf["channel"]) * len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * len(self.tcConf["freq_rx"]) * len(self.tcConf["bbFreq"])
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
            self.dut = Dut(chan=chan, simulate=self.simulate) #dut drivers init

            #configuration dut
            self.dut.mode = "RX"
            self.dut.preamp0 = "LNA"
            self.dut.preamp1 = "LNA"
            self.dut.preamp2 = "LNA"

            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for power in self.tcConf["power"]:
                    if self.status is st().ABORTING:
                        break
                    self.RFSigGen.power = power + RFSigGenOffset["smb100a"] #configure power


                    for freq_rx, filter_rx in zip(self.tcConf["freq_rx"],self.tcConf["filter_rx"]):
                        if self.status is st().ABORTING:
                            break
                        self.dut.freqRx = freq_rx         #configure dut freq
                        self.dut.filterRx = filter_rx

                        for dfreq in self.tcConf["bbFreq"]:
                            if self.status is st().ABORTING:
                                break
                            self.RFSigGen.freq = freq_rx + dfreq                    

                            #update progress
                            self.iteration += 1
                            self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))

                            #start measurement
                            result = self.dut.irrSin(freqBBHz = dfreq)

                            #write measures
                            if result["rssi"] != "NA":
                                gain = float(result["rssi"]) - float(power)
                            else:
                                gain = "NA"
                            conf = {
                                "vdd":vdd,
                                "power":power,
                                "freq_rx":freq_rx,
                                "filter_rx":filter_rx,
                                "temp":self.temp,
                                "baseband":dfreq
                            }
                            result = {
                                "rssi":result["rssi"],
                                "irr":result["irr"],
                                "dGain":result["dGain"],
                                "dPhase":result["dPhase"],
                                "gain":gain
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
        self.logger.info("Init ate")
        self.DCPwr = DCPwr(simulate=self.simulate)
        self.RFSigGen = RFSigGen(simulate=self.simulate)
        self.Swtch = Swtch(simulate=self.simulate)
        self.Clim = ClimCham(simulate=self.simulate)

        #ate configuration
        self.Swtch.setSwitch(sw2 = 4, sw3 = 3, sw4 = 1)
        self.RFSigGen.power = -130
        self.RFSigGen.status = 1

    def __writeMeasure(self, conf, result):
        return {
            "date-measure":time.time(),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":__version__,
            "status":self.status,
            "input-parameters":conf,
            "dut-info":self.dut.info,
            "ate-result":{
                "DCPwr":self.DCPwr.info,
                "Clim":self.Clim.info,
                "RFSigGen":self.RFSigGen.info
            },
            "dut-result":result
        }
