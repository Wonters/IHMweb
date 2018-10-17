# coding=UTF-8

from ..testcases.baseTestCase import baseTestCase
from ..testcases.baseTestCase import st
from ..drivers.ate.DCPwr import DCPwr
from ..drivers.ate.SpecAn import SpecAn
from ..drivers.ate.PwrMeter import PwrMeter
from ..drivers.ate.Swtch import Swtch
from ..drivers.ate.ClimCham import ClimCham
from ..drivers.dut import Dut
from .. import __version__
import time

class txExcursion(baseTestCase):
    def __init__(self, temp, simulate):
        baseTestCase.__init__(self, temp, simulate)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.tcConf["channel"]) * len(self.tcConf["voltage"]) * len(self.tcConf["freq_tx"]) * len(self.tcConf["bbFreq"]) * len(self.tcConf["att"])
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
            self.dut = Dut(chan=chan, simulate=self.simulate)  #dut drivers init

            #configuration dut
            self.dut.mode = "TX"


            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for freq_tx, filter_tx in zip(self.tcConf["freq_tx"],self.tcConf["filter_tx"]):
                    if self.status is st().ABORTING:
                        break
                    self.dut.freqTx = freq_tx
                    self.PwrMeter.freq = freq_tx
                    self.SpecAn.freqCenter = freq_tx
                    self.dut.filterTx = filter_tx

                    #measure of OL frequency
                    self.dut.playBBSine(atten=self.tcConf["inputAttCal"], freqBBHz=self.tcConf["bbFreqCal"])
                    self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average
                    self.SpecAn.markerSearchLimit(freqleft = freq_tx + (self.tcConf["bbFreqCal"] - self.tcConf["searchLimit"]) , freqright = freq_tx + (self.tcConf["bbFreqCal"] +  self.tcConf["searchLimit"]))
                    OLfreq = self.SpecAn.markerPeakSearch()[0] - self.tcConf["bbFreqCal"]
                    self.dut.stopBBSine()

                    #Center SA
                    self.SpecAn.freqCenter = OLfreq


                    for dfreq in self.tcConf["bbFreq"]:
                        if self.status is st().ABORTING:
                            break


                        for att in self.tcConf["att"]:
                            if self.status is st().ABORTING:
                                break

                            #update progress
                            self.iteration += 1
                            self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))
                            self.logger.info("input parameters : {0}C, chan {1}, {2}V, {3}Hz(DUT), {4}Hz(BBHz), atten {5}".format(self.temp, chan, vdd, freq_tx, dfreq, att))

                            #configure DUT
                            self.dut.playBBSine(freqBBHz = dfreq, atten = att)

                            #configure ATE
                            self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average

                            #start measurement
                            resultPower = self.PwrMeter.power
                            #measure carrier
                            self.SpecAn.markerSearchLimit(freqleft = OLfreq + (dfreq - self.tcConf["searchLimit"]) , freqright = OLfreq + (dfreq +  self.tcConf["searchLimit"]))
                            resultCarrier = self.SpecAn.markerPeakSearch()       #place marker
                            #measure image
                            self.SpecAn.markerSearchLimit(freqleft = OLfreq + (-dfreq - self.tcConf["searchLimit"]) , freqright = OLfreq + (-dfreq +  self.tcConf["searchLimit"]))
                            resultImage = self.SpecAn.markerPeakSearch()       #place marker
                            #measure OL
                            self.SpecAn.markerSearchLimit(freqleft = OLfreq -  self.tcConf["searchLimit"] , freqright = OLfreq +  self.tcConf["searchLimit"])
                            resultOL = self.SpecAn.markerPeakSearch()       #place marker

                            #write measures
                            conf = {
                                "vdd":vdd,
                                "freq_tx":freq_tx,
                                "filter_tx":filter_tx,
                                "baseband":dfreq,
                                "atten":att,
                                "temp":self.temp
                            }
                            dut_result = {
                                "carrier_x":resultCarrier[0],
                                "carrier_y":resultCarrier[1],
                                "image_x":resultImage[0],
                                "image_y":resultImage[1],
                                "image_dbc":resultImage[1]-resultCarrier[1],
                                "ol_x":resultOL[0],
                                "ol_y":resultOL[1],
                                "power":resultPower
                            }
                            self.db.writeDataBase(self.__writeMeasure(conf, dut_result))
                            
                            #stop measurement
                            self.dut.stopBBSine()

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
        self.Clim = ClimCham(simulate=self.simulate)

        #configure SpecAn
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
        self.SpecAn.refLvl = self.tcConf["refLvl"]
        self.SpecAn.rbw = self.tcConf["rbw"]
        self.SpecAn.vbw = self.tcConf["vbw"]
        self.SpecAn.freqSpan = self.tcConf["span"]

    def __writeMeasure(self, conf, dut_result):
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
                "PwrMeter":self.PwrMeter.info,
                "ClimCham":self.Clim.info,
                "SpecAn":self.SpecAn.info
            },
            "dut-result":dut_result
        }
