# coding=UTF-8

from ..testcases.baseTestCase import baseTestCase
from ..testcases.baseTestCase import st
from ..drivers.ate.DCPwr import DCPwr
from ..drivers.ate.SpecAn import SpecAn
from ..drivers.ate.Swtch import Swtch
from ..drivers.dut import Dut
from ..tools.log import get_logger, AcbbsError
from .. import __version__
import time

class txPowVsFreq(baseTestCase):
    def __init__(self, temp, simulate, conf, comment, date, channel):
        baseTestCase.__init__(self, temp, simulate, conf, comment, date, channel)

        #Tc version
        self.tcVersion = "1.0.0"

        #set freq list
        self.freq_tx = {}
        len_freq = 0
        for filter_tx_key, filter_tx_value in self.tcConf["filter_tx"].items():
            self.freq_tx[filter_tx_key] = []
            for i in range (filter_tx_value["freq_tx_min"], filter_tx_value["freq_tx_max"] + 1, self.tcConf["freq_tx_step"]):
                self.freq_tx[filter_tx_key].append(i)
                len_freq += 1


        #calcul iterations number
        self.iterationsNumber = len(self.channel) * len(self.tcConf["voltage"]) * len_freq * len(self.tcConf["att"]) * len(self.tcConf["dFreq"])
        self.log.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.log.info("Start loop of \"{0}\"".format(self.__class__.__name__))
        for chan in self.channel:
            if self.status is st().ABORTING:
                break
            swtch_loss = self.Swtch.setSwitch(sw1 = chan)           #configure Swtch channel
            self.DCPwr.setChan(dutChan = chan)                      #configure DCPwr channel
            self.dut = Dut(chan=chan, simulate=self.simulate)       #dut drivers init

            #configuration dut
            self.dut.mode = "TX"

            #set SpecAn Offset
            self.SpecAn.refLvlOffset = swtch_loss["fsv-fswr"]
            self.SpecAn.refLvl = self.tcConf["refLvl"]


            for vdd in self.tcConf["voltage"]:
                if self.status is st().ABORTING:
                    break
                self.DCPwr.voltage = vdd               #configure voltage


                for filter_tx in self.freq_tx.keys():
                    if self.status is st().ABORTING:
                        break
                    self.dut.filterTx = filter_tx


                    for freq_tx in self.freq_tx[filter_tx]:
                        if self.status is st().ABORTING:
                            break
                        self.dut.freqTx = freq_tx
                        self.SpecAn.freqCenter = freq_tx


                        for att in self.tcConf["att"]:
                            if self.status is st().ABORTING:
                                break


                            for dfreq in self.tcConf["dFreq"]:
                                if self.status is st().ABORTING:
                                    break

                                #update progress
                                self.iteration += 1
                                self.log.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))
                                self.log.info("input parameters : {0}C, chan {1}, {2}V, {3}Hz(DUT), atten {4}".format(self.temp, chan, vdd, freq_tx, att))

                                #configure DUT
                                self.dut.playBBSine(freqBBHz = dfreq, atten = att)

                                #configure ATE
                                self.SpecAn.averageCount(self.tcConf["countAverage"])   #get an average

                                #measure carrier
                                self.SpecAn.markerSearchLimit(freqleft = freq_tx + (dfreq - self.tcConf["searchLimit"]) , freqright = freq_tx + (dfreq +  self.tcConf["searchLimit"]))
                                resultCarrier = self.SpecAn.markerPeakSearch()       #place marker

                                #write measures
                                conf = {
                                    "Supply_voltage_(V)":vdd,
                                    "RF_Output_Frequency_(Hz)":freq_tx,
                                    "DUT_TX_Filter_ID":int(filter_tx),
                                    "DUT_TX_Level_Control":att,
                                    "Oven_Temperature_(C)":self.temp
                                }
                                dut_result = {
                                    "DUT_TX_Carrier_Frequency_(Hz)":resultCarrier[0],
                                    "DUT_TX_Carrier_Power_(dBm)":resultCarrier[1]
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
        self.log.debug("Init ate")
        self.DCPwr = DCPwr(simulate=self.simulate)
        self.SpecAn = SpecAn(simulate=self.simulate)
        self.Swtch = Swtch(simulate=self.simulate)
        self.Swtch.setSwitch(sw2 = 4, sw3 = 4, sw4 = 2)

        #configure SpecAn
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
        self.SpecAn.rbw = self.tcConf["rbw"]
        self.SpecAn.vbw = self.tcConf["vbw"]
        self.SpecAn.freqSpan = self.tcConf["span"]

    def __writeMeasure(self, conf, dut_result):
        return {
            "comment":self.comment,
            "config":self.tcConf,
            "date-measure":int(time.time()),
            "date-tc":self.date,
            "tc_version":self.tcVersion,
            "acbbs_version":__version__,
            "status":self.status,
            "input-parameters":conf,
            "dut-info":self.dut.info,
            "ate-result":{
                "DCPwr":self.DCPwr.info,
                "SpecAn":self.SpecAn.info
            },
            "dut-result":dut_result
        }
