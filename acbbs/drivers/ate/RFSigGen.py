# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from vxi11 import Instrument

class RFSigGen(object):
    class _simulate(object):
        def __init__(self):
            return
        def write(self, val):
            return '0'
        def read(self, val, timeout=None):
            return '0'

    def __init__(self, simulate = False):

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.sigGenConf = self.conf.getConfiguration()

        if not simulate:
            self.logger.info("Init RFSigGen")
            self.simulate = False
            try :
                #Initialise and configure ATE
                self.inst = Instrument(sig_gen)
                inst.write("*CLS")
                inst.write("*RST")
            except :
                raise AcbbsError("RFSigGen Connection error", log = self.logger)
            Ps_hmp4040.powerDevice1.write("OUTP:GEN ON\n")
            Ps_hmp4040.powerDevice2.write("OUTP:GEN ON\n")
        else :
            self.simulate = True
            self.logger.info("Init RFSigGen in Simulate")
            self.inst = self._simulate()

    @property
    def errors(self):
        if not self.simulate:
            pass
        else:
            return []

    @property
    def reference(self):
        if not self.simulate:
            pass
        else:
            return "XXXXXX"

    @property
    def version(self):
        if not self.simulate:
            pass
        else:
            return "1.0.0"

    @property
    def status(self):
        if not self.simulate:
            pass
        else:
            return "STBY"

    @status.setter
    def status(self, value):
        self.inst.write(":OUTP:STATE {0}".format(value))

    @property
    def power(self):
        if not self.simulate:
            pass
        else:
            return "-100"

    @power.setter
    def power(self, value):
        self.inst.write(":SOUR:POW:LEV:IMM:AMPL {0}".format(value + self.sigGenConf["cableLoss"]))

    @property
    def freq(self):
        if not self.simulate:
            pass
        else:
            return "868000000"

    @freq.setter
    def freq(self, value):
        self.inst.write(":SOUR:FREQ:CW {0}".format(value))

    def __readWrite(self, cmd = None, value = None):
        pass

    def __wait(self):
        pass
