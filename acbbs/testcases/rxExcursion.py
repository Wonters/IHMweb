# coding=UTF-8

from ..testcases.baseTestCase import baseTestCase, st
from ..drivers.ate.DCPwr import DCPwr
from ..drivers.ate.RFSigGen import RFSigGen
from ..drivers.ate.Swtch import Swtch
from ..drivers.dut import Dut
from .. import __version__
import time

class rxExcursion(baseTestCase):
    def __init__(self, temp, simulate, conf, comment, date, channel):
        baseTestCase.__init__(self, temp, simulate, conf, comment, date, channel)

        #Tc version
        self.tcVersion = "1.0.0"

        #get backoff
        self.backoff = self.conf.getBackoff(self.tcConf["backoff"])

        #calcul iterations number
        self.iterationsNumber = len(self.channel) * len(self.tcConf["voltage"]) * len(self.tcConf["power"]) * len(self.tcConf["freq_rx"]) * len(self.tcConf["bbFreq"]) * len(self.tcConf["backoff"])
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.channel:
            if self.status is st().ABORTING:
                break
            RFSigGenOffset = self.Swtch.setSwitch(sw1 = chan) #configure Swtch channel
            self.DCPwr.setChan(dutChan = chan)         #configure DCPwr channel
            self.dut = Dut(chan=chan, simulate=self.simulate) #dut drivers init

            #configuration dut
            self.dut.mode = "RX"

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

                            #measure refLevel
                            #configure DUT
                            self.dut.preamp0 = self.backoff[0][1]
                            self.dut.preamp1 = self.backoff[0][2]
                            self.dut.preamp2 = self.backoff[0][3]

                            #start measurement
                            refLevel = self.dut.irrSin(freqBBHz = dfreq)["rssi"]

                            for backoff in self.backoff:
                                if self.status is st().ABORTING:
                                    break                           

                                #update progress
                                self.iteration += 1
                                self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))
                                self.logger.info("input parameters : {0}C, chan {1}, {2}V, {3}dBm, {4}Hz(Gen), {5}Hz(BBHz), {6}".format(self.temp, chan, vdd, power, freq_rx, dfreq, backoff))

                                #configure ATE
                                self.dut.preamp0 = backoff[1]
                                self.dut.preamp1 = backoff[2]
                                self.dut.preamp2 = backoff[3]

                                #start measurement
                                result = self.dut.irrSin(freqBBHz = dfreq)

                                if result["rssi"] != "NA" and refLevel != "NA":
                                    #write measures
                                    conf = {
                                        "Supply_voltage_(V)":vdd,
                                        "RF_Input_Power_(dBm)":power,
                                        "RF_Input_Frequency_(Hz)":freq_rx,
                                        "DUT_RX_Filter_ID":filter_rx,
                                        "Oven_Temperature_(C)":self.temp,
                                        "RX_Baseband_Frequency_(Hz)":dfreq,
                                        "DUT_Backoff_ID":backoff[0]
                                    }
                                    dut_result = {
                                        "DUT_RX_Max_Power_(dBtIQ)":refLevel,
                                        "DUT_RSSI_Vs_Backoff_(dBtIQ)":result["rssi"],
                                        "DUT_RX_IRR_(dBc)":result["irr"],
                                        "DUT_RX_dGain_(degtIQ)":result["dGain"],
                                        "DUT_RX_dPhase_(degtIQ)":result["dPhase"],
                                        "DUT_RX_Backoff_Gain_(dB)":refLevel - result["rssi"],
                                        "DUT_Gain_Vs_Backoff_(dB)":float(result["rssi"]) - float(power)
                                    }
                                    self.db.writeDataBase(self.__writeMeasure(conf, dut_result))


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

        #ate configuration
        self.Swtch.setSwitch(sw2 = 4, sw3 = 3, sw4 = 1)
        self.RFSigGen.power = -130
        self.RFSigGen.status = 1

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
                "RFSigGen":self.RFSigGen.info
            },
            "dut-result":dut_result
        }
