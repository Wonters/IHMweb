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

class txOLFrequency(baseTestCase):
    def __init__(self, temp, simulate, conf, comment, date, channel):
        baseTestCase.__init__(self, temp, simulate, conf, comment, date, channel)

        #parse frequencies
        freq_tx, freq_rx = self.conf.getFrequencies(self.tcConf["radio_configuration"])        
        if len(self.tcConf["freq_tx"]) == 0:
            self.tcConf["freq_tx"] = freq_tx

        #parse filters
        filter_tx, filter_rx = self.conf.getFilters(self.tcConf["radio_configuration"])
        if len(self.tcConf["filter_tx"]) == 0:
            self.tcConf["filter_tx"] = filter_tx

        #check for filters and frequencies number
        if len(self.tcConf["filter_tx"]) != len(self.tcConf["freq_tx"]):
            raise AcbbsError("Errors: filter_tx and freq_tx lists has not the same size.")

        #Tc version
        self.tcVersion = "1.0.0"

        #calcul iterations number
        self.iterationsNumber = len(self.channel) * len(self.tcConf["voltage"]) * len(self.tcConf["freq_tx"])
        self.logger.info("Number of iteration : {0}".format(self.iterationsNumber))

    def run(self):
        #update status
        self.status = st().RUNNING

        #start loop
        self.logger.info("Start loop of \"{0}\"".format(self.__class__.__name__))
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


                for freq_tx, filter_tx in zip(self.tcConf["freq_tx"],self.tcConf["filter_tx"]):
                    if self.status is st().ABORTING:
                        break
                    self.dut.freqTx = freq_tx
                    self.dut.filterTx = filter_tx
                    self.SpecAn.freqCenter = freq_tx

                    #update progress
                    self.iteration += 1
                    self.logger.info("iteration : {0}/{1}".format(self.iteration, self.iterationsNumber))
                    self.logger.info("input parameters : {}C, chan {}, {}V, {}Hz(DUT)".format(self.temp, chan, vdd, freq_tx))

                    #configure DUT
                    self.dut.playBBSine(freqBBHz = 10000, atten = 28, dB = -80)

                    #configure ATE
                    self.SpecAn.freqSpan = 200000

                    #get frequency
                    self.SpecAn.markerSet()
                    self.SpecAn.markerPeakSearch()
                    time.sleep(10)
                    resultOLFrequency = self.SpecAn.markerGetFreqAccuracy()
                    delta = round(resultOLFrequency-freq_tx,1)

                    #write measures
                    conf = {
                        "Supply_voltage_(V)":vdd,
                        "RF_Output_Frequency_(Hz)":freq_tx,
                        "DUT_TX_Filter_ID":filter_tx,
                        "Oven_Temperature_(C)":self.temp
                    }
                    dut_result = {
                        "DUT_TX_OL_Frequency_(Hz)":resultOLFrequency,
                        "DUT_TX_OL_Frequency_Delta_(Hz)":delta,
                        "DUT_TX_OL_Frequency_Variation_(PPM)":round((delta * 1000000) / freq_tx, 2)
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
        self.Swtch = Swtch(simulate=self.simulate)
        self.Swtch.setSwitch(sw2 = 4, sw3 = 4, sw4 = 2)

        #configure SpecAn
        self.SpecAn.inputAtt = self.tcConf["inputAtt"]
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
