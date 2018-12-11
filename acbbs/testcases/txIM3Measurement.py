# coding=UTF-8

from ..testcases.baseTestCase import baseTestCase
from ..testcases.baseTestCase import st
from ..drivers.ate.DCPwr import DCPwr
from ..drivers.ate.SpecAn import SpecAn
from ..drivers.ate.PwrMeter import PwrMeter
from ..drivers.ate.Swtch import Swtch
from ..drivers.dut import Dut
from .. import __version__
import time

class txIM3Measurement(baseTestCase):
    def __init__(self, temp, simulate, conf, comment, date, channel):
        baseTestCase.__init__(self, temp, simulate, conf, comment, date, channel)

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.channel) * len(self.tcConf["voltage"]) * len(self.tcConf["freq_tx"]) * len(self.tcConf["att"])
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.channel:
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

                    #calcul F1 and F2
                    freqF1 = OLfreq + self.tcConf["bbFreq1"]
                    freqF2 = OLfreq + self.tcConf["bbFreq2"]

                    #Center SA
                    self.SpecAn.freqCenter = (freqF1 + freqF2) / 2


                    for att in self.tcConf["att"]:
                        if self.status is st().ABORTING:
                            break

                        #update progress
                        self.iteration += 1
                        self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))
                        self.logger.info("input parameters : {0}C, chan {1}, {2}V, {3}Hz(DUT), atten {4}".format(self.temp, chan, vdd, freq_tx, att))

                        #configure DUT
                        self.dut.playBBSine(freqBBHz = [self.tcConf["bbFreq1"], self.tcConf["bbFreq2"]], atten = att)

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

                        #write measures
                        conf = {
                            "Supply_voltage_(V)":vdd,
                            "RF_Output_Frequency_(Hz)":freq_tx,
                            "DUT_TX_Filter_ID":filter_tx,
                            "TX_Baseband1_Frequency_(Hz)":self.tcConf["bbFreq1"],
                            "TX_Baseband2_Frequency_(Hz)":self.tcConf["bbFreq2"],
                            "DUT_TX_Level_Control":att,
                            "Oven_Temperature_(C)":self.temp
                        }
                        dut_result = {
                            "DUT_TX_Baseband1_Frequency_(Hz)":F1[0],
                            "DUT_TX_Baseband1_Power_(dBm)":F1[1],
                            "DUT_TX_Baseband2_Frequency_(Hz)":F2[0],
                            "DUT_TX_Baseband2_Power_(dBm)":F2[1],
                            "DUT_TX_IM3_p_Frequency_(Hz)":F1F2[0],
                            "DUT_TX_IM3_p_Power_(dBm)":F1F2[1],
                            "DUT_TX_IM3_m_Frequency_(Hz)":F2F1[0],
                            "DUT_TX_IM3_m_Power_(dBm)":F2F1[1],
                            "DUT_TX_Total_Output_Power_(dBm)":resultPower,
                            "DUT_TX_OIP3_(dBm)":F1[1]+(F1[1]-F2F1[1])/2
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

        #configure SpecAn
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
        self.SpecAn.refLvl = self.tcConf["refLvl"]
        self.SpecAn.rbw = self.tcConf["rbw"]
        self.SpecAn.vbw = self.tcConf["vbw"]
        self.SpecAn.freqSpan = self.tcConf["span"]

    def __writeMeasure(self, conf, dut_result):
        return {
            "comment":self.comment,
            "config":self.tcConf,
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
                "SpecAn":self.SpecAn.info
            },
            "dut-result":dut_result
        }
