# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.Swtch import *

class txPowVsAtt(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, temp, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        attIter = 0
        for i in range(self.tcConf["attLow"], self.tcConf["attHigh"] + 1, self.tcConf["attStep"]):
            attIter += 1
        self.iterationsNumber = len(self.tcConf["channel"]) * len(self.tcConf["voltage"]) * len(self.tcConf["freq"]) * attIter
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

            #configuration dut
            self.dut.mode = "TX"


            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for freq in self.tcConf["freq"]:
                    if self.status is st().ABORTING:
                        break
                    self.dut.freqTx = freq
                    self.PwrMeter.freq = freq + self.tcConf["bbFreq"]


                    for att in range(self.tcConf["attLow"], self.tcConf["attHigh"] + 1, self.tcConf["attStep"]):
                        if self.status is st().ABORTING:
                            break

                        #update progress
                        self.iteration += 1

                        #configure DUT
                        self.dut.playBBSine(freqBBHz = self.tcConf["bbFreq"], atten = att, timeSec = "10")

                        #mesure Tx power
                        #configure ATE
                        self.SpecAn.freqCenter = freq + self.tcConf["bbFreq"]
                        self.SpecAn.markerSearchLimit(marker = 1, freqleft = freq + self.tcConf["bbFreq"] - 1500, freqright = freq + self.tcConf["bbFreq"] + 1500) #place limit search
                        self.SpecAn.averageCount(self.tcConf["countAverage"])              #get an average

                        #start measurement
                        resultMarkerPeak1 = self.SpecAn.markerPeakSearch(marker = 1)       #place marker
                        resultPower1 = self.PwrMeter.power

                        #mesure OlLeakage
                        #configure ATE
                        self.SpecAn.freqCenter = self.tcConf["OlLeakage"]
                        self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average
                        self.SpecAn.markerSearchLimit(marker = 2, freqleft = self.tcConf["OlLeakage"] - 1000, freqright = self.tcConf["OlLeakage"] + 1000) #place limit search

                        #start measurement
                        resultMarkerPeak2 = self.SpecAn.markerPeakSearch(marker = 2)       #place marker
                        resultPower2 = self.PwrMeter.power

                        #stop measurement
                        self.dut.stopBBSine()

                        #write measures
                        conf = {
                            "vdd":vdd,
                            "freq":freq,
                            "baseband":self.tcConf["bbFreq"],
                            "Olleakage":self.tcConf["OlLeakage"],
                            "atten":att,
                            "temp":self.temp
                        }
                        result = {
                            "marker_x1":resultMarkerPeak1[0],
                            "marker_y1":resultMarkerPeak1[1],
                            "power1":resultPower1,
                            "marker_xol":resultMarkerPeak2[0],
                            "marker_yol":resultMarkerPeak2[1],
                            "power2":resultPower2
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
        self.SpecAn = SpecAn(simulate=self.simulate)
        self.Swtch = Swtch(simulate=self.simulate)
        self.Swtch.setSwitch(sw2 = 4, sw3 = 4, sw4 = 2)

        #configure SpecAn
        self.SpecAn.refLvlOffset = self.tcConf["refLvlOffset"]
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
        self.SpecAn.refLvl = self.tcConf["refLvl"]
        self.SpecAn.rbw = self.tcConf["rbw"]
        self.SpecAn.vbw = self.tcConf["vbw"]
        self.SpecAn.span = self.tcConf["span"]
        self.SpecAn.sweep = self.tcConf["sweep"]

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
                "PwrMeter":self.PwrMeter.info,
                "SpecAn":self.SpecAn.info
            },
            "dut-result":result
        }
