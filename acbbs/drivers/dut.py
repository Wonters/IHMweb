# coding=UTF-8
from acbbs.tools.log import *
from acbbs.testcases.baseTestCase import *
from acbbs.tools.dataBase import *

class dut(object):
    def __init__(self, simulate = False):
        self.address = None
        self.channel = None
        self.radioFw = None
        self.radioHw = None
        self.tapFw = None
        self.tapHW = None
        self.tapId = None
        self.tmpHw = None
        self.tmpVendor = None

    def address(self):
        """


        @return  :
        @author
        """
        pass

    def radioFw(self):
        """


        @return  :
        @author
        """
        pass

    def radioHw(self):
        """


        @return  :
        @author
        """
        pass

    def tapFw(self):
        """


        @return  :
        @author
        """
        pass

    def tapHw(self):
        """


        @return  :
        @author
        """
        pass

    def tapId(self):
        """


        @return  :
        @author
        """
        pass

    def tpmHw(self):
        """


        @return  :
        @author
        """
        pass

    def tpmVendor(self):
        """


        @return  :
        @author
        """
        pass

    def allMeasure(self):
        """


        @return  :
        @author
        """
        pass

    def allMeasureAvailable(self):
        """


        @return  :
        @author
        """
        pass

    def freqTx(self):
        """


        @return  :
        @author
        """
        pass

    def freqRx(self):
        """


        @return  :
        @author
        """
        pass

    def mode(self):
        """


        @return  :
        @author
        """
        pass

    def preamp0(self):
        """


        @return  :
        @author
        """
        pass

    def preamp1(self):
        """


        @return  :
        @author
        """
        pass

    def preamp2(self):
        """


        @return  :
        @author
        """
        pass

    def nxpRegister(self, group = 0, index = 0):
        """


        @param int group :
        @param int index :
        @return  :
        @author
        """
        pass

    def playBBSine(self, freqBBHz = 20000, timeSec = 1, atten = 10):
        """


        @param int freqBBHz :
        @param int timeSec :
        @param int atten :
        @return  :
        @author
        """
        pass

    def stopBBSine(self):
        """


        @return  :
        @author
        """
        pass

    def playBBNoise(self, bwBBHz = 20000, timeSec = 1, atten = 10):
        """


        @param int bwBBHz :
        @param int timeSec :
        @param int atten :
        @return  :
        @author
        """
        pass

    def stopBBNoise(self):
        """


        @return  :
        @author
        """
        pass

    def rssiSin(self, freqBBHz = 20000):
        """


        @param int freqBBHz :
        @return  :
        @author
        """
        pass

    def irrSin(self, freqBBHz = 20000):
        """


        @param int freqBBHz :
        @return  :
        @author
        """
        pass

    def __launchCmd(self, uri, get = True, payloadJson = None, payloadData = None, stream = False, callback = None):
        """


        @param string uri :
        @param bool get :
        @param  payloadJson :
        @param  payloadData :
        @param bool stream :
        @param  callback :
        @return  :
        @author
        """
        pass

    def __launchGetJson(self, uri):
        """


        @param string uri :
        @return  :
        @author
        """
        pass
