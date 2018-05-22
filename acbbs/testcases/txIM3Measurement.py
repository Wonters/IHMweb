# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.Swtch import *

class txIM3Measurement(baseTestCase):
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
            self.dut = dut(chan=chan, simulate=self.simulate)  #dut drivers init

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
                    self.PwrMeter.freq = freq
                    self.SpecAn.freqCenter = freq

                    #measure of OL frequency
                    self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average
                    self.SpecAn.runSingle()
                    OLfreq = self.SpecAn.markerPeakSearch()[0]

                    #calcul F1 and F2
                    freqF1 = OLfreq + self.tcConf["bbFreq1"]
                    freqF2 = OLfreq + self.tcConf["bbFreq2"]

                    #Center SA
                    self.SpecAn.freqCenter = (freqF1 + freqF2) / 2


                    for att in range(self.tcConf["attLow"], self.tcConf["attHigh"] + 1, self.tcConf["attStep"]):
                        if self.status is st().ABORTING:
                            break

                        #update progress
                        self.iteration += 1

                        #configure DUT
                        self.dut.playBBSine(freqBBHz = [self.tcConf["bbFreq1"], self.tcConf["bbFreq2"]], atten = att, timeSec = "10")

                        #configure ATE
                        self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average

                        #start measurement
                        resultPower = self.PwrMeter.power

                        #calcul searchlimit
                        searchLimitLeft1 = freqF1 - self.tcConf["searchLimit"]
                        searchLimitRight1 = freqF1 + self.tcConf["searchLimit"]

                        searchLimitLeft2 = freqF2 - self.tcConf["searchLimit"]
                        searchLimitRight2 = freqF2 + self.tcConf["searchLimit"]

                        searchLimitLeft3 = (2*freqF1 - freqF2) - self.tcConf["searchLimit"]
                        searchLimitRight3 = (2*freqF1 - freqF2) + self.tcConf["searchLimit"]

                        searchLimitLeft4 = (2*freqF2 - freqF1) - self.tcConf["searchLimit"]
                        searchLimitRight4 = (2*freqF2 - freqF1) + self.tcConf["searchLimit"]

                        #place limitsearch and do measures
                        self.SpecAn.markerSearchLimit(freqleft = searchLimitLeft1 , freqright = searchLimitRight1)
                        F1 = self.SpecAn.markerPeakSearch(marker = 1)
                        self.SpecAn.markerSearchLimit(freqleft = searchLimitLeft2 , freqright = searchLimitRight2)
                        F2 = self.SpecAn.markerPeakSearch(marker = 2)
                        self.SpecAn.markerSearchLimit(freqleft = searchLimitLeft3 , freqright = searchLimitRight3)
                        F1F2 = self.SpecAn.markerPeakSearch(marker = 3)
                        self.SpecAn.markerSearchLimit(freqleft = searchLimitLeft4 , freqright = searchLimitRight4)
                        F2F1 = self.SpecAn.markerPeakSearch(marker = 4)

                        #stop measurement
                        self.dut.stopBBSine()

                        #write measures
                        conf = {
                            "vdd":vdd,
                            "freq":freq,
                            "baseband1":self.tcConf["bbFreq1"],
                            "baseband2":self.tcConf["bbFreq2"],
                            "atten":att,
                            "temp":self.temp
                        }
                        result = {
                            "F1_f":F1[0],
                            "F1_p":F1[1],
                            "F2_f":F2[0],
                            "F2_p":F2[1],
                            "F1F2_f":F1F2[0],
                            "F1F2_p":F1F2[1],
                            "F2F1_f":F2F1[0],
                            "F2F1_p":F2F1[1],
                            "power":resultPower,
                            "ip3":F1[1]+(F1[1]-F2F1[1])/2
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
        self.SpecAn = SpecAn(simulate=self.simulate)
        if self.tcConf["pwmeter"] is 1:
            self.PwrMeter = PwrMeter(simulate=self.simulate)
        else:
            self.PwrMeter = PwrMeter(simulate=True)
        self.Swtch = Swtch(simulate=self.simulate)
        self.Swtch.setSwitch(sw2 = 4, sw3 = 4, sw4 = 2)

        #configure SpecAn
        self.SpecAn.refLvlOffset = self.tcConf["refLvlOffset"]
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
        self.SpecAn.refLvl = self.tcConf["refLvl"]
        self.SpecAn.rbw = self.tcConf["rbw"]
        self.SpecAn.vbw = self.tcConf["vbw"]
        self.SpecAn.freqSpan = self.tcConf["span"]

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
