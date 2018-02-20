# coding=UTF-8
from acbbs.tools.dataBase import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.Swtch import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.tools.log import *
from acbbs.testcases.rxGainLNAs import *
from acbbs.tools.configurationFile import *

class baseTestCase(object):
    def __init__(self):
        self.progress = None
        self.status = None

    def getProgress(self):
        return self.progress

    def getStatus(self):
        return self.status

    def run(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def abort(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def tcInit(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def __getATEInformations(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()
