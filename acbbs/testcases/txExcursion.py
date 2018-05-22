# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.Swtch import *

class txExcursion(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, temp, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #get att list
        self.attlist = []
        if len(self.tcConf["attlist"]) == 0:
            for att in range(self.tcConf["attLow"], self.tcConf["attHigh"] + 1, self.tcConf["attStep"]):
                self.attlist.append(att)
        else:
            self.attlist = self.tcConf["attlist"]


        #calcul iterations number
        self.bbFreq = []
        attIter = 0
        for i in range(self.tcConf["bbFreqLow"], self.tcConf["bbFreqHigh"] + 1, self.tcConf["bbFreqStep"]):
            if abs(i) >  self.tcConf["searchLimit"] * 2:
                self.bbFreq.append(i)
        self.iterationsNumber = len(self.tcConf["channel"]) * len(self.tcConf["voltage"]) * len(self.tcConf["freq"]) * len(self.bbFreq) * len(self.attlist)
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

                    #Center SA
                    self.SpecAn.freqCenter = OLfreq


                    for dfreq in self.bbFreq:
                        if self.status is st().ABORTING:
                            break


                        for att in self.attlist:
                            if self.status is st().ABORTING:
                                break

                            #update progress
                            self.iteration += 1

                            #configure DUT
                            self.dut.playBBSine(freqBBHz = dfreq, atten = att, timeSec = "10")

                            #configure ATE
                            self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average

                            #start measurement
                            resultPower = self.PwrMeter.power
                            #measure carrier and image
                            self.SpecAn.markerSearchLimit(freqleft = OLfreq + (dfreq - self.tcConf["searchLimit"]) , freqright = OLfreq + (dfreq +  self.tcConf["searchLimit"]))
                            resultCarrier = self.SpecAn.markerPeakSearch()       #place marker
                            resultImage = self.SpecAn.markerDelta(mode = "REL", delta = -2*dfreq)
                            #measure OL
                            self.SpecAn.markerSearchLimit(freqleft = OLfreq -  self.tcConf["searchLimit"] , freqright = OLfreq +  self.tcConf["searchLimit"])
                            resultOL = self.SpecAn.markerPeakSearch()       #place marker

                            #stop measurement
                            self.dut.stopBBSine()

                            #write measures
                            conf = {
                                "vdd":vdd,
                                "freq":freq,
                                "baseband":dfreq,
                                "atten":att,
                                "temp":self.temp
                            }
                            result = {
                                "carrier_x":resultCarrier[0],
                                "carrier_y":resultCarrier[1],
                                "image_x":-2*dfreq,
                                "image_y":resultImage,
                                "ol_x":resultOL[0],
                                "ol_y":resultOL[1],
                                "power":resultPower
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
