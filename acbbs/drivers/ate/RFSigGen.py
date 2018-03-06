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
            self.logger.info("Init RFSigGen in Simulate")
            self.inst = self._simulate()

    def getErrors(self):
        return []

    @property
    def reference(self):
        return ""

    @property
    def version(self):
        return ""

    @property
    def status(self):
        return ""

    @status.setter
    def status(self, value):
        self.inst.write(":OUTP:STATE {0}".format(value))

    @property
    def power(self):
        return ""

    @power.setter
    def power(self, value):
        self.inst.write(":SOUR:POW:LEV:IMM:AMPL {0}".format(value + self.sigGenConf["cableLoss"]))

    @property
    def freq(self):
        return ""

    @freq.setter
    def freq(self, value):
        self.inst.write(":SOUR:FREQ:CW {0}".format(value))

    def __readWrite(self, cmd = None, value = None):
        """


        @param  cmd :
        @param  value :
        @return  :
        @author
        """
        pass

    def __wait(self):
        """


        @return  :
        @author
        """
        pass
