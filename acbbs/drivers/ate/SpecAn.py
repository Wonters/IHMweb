# coding=UTF-8
from acbbs.tools.log import *

class SpecAn(object):
    def __init__(self, simulate = False):
        """


        @param bool simulate :
        @return  :
        @author
        """
        pass

    def limitLineCreation(self, name = None, value = None):
        """


        @param string name :
        @param  value :
        @return  :
        @author
        """
        pass

    def limitGabaritCreation(self, name = None, freqTab = None, limitTab = None):
        """


        @param string name :
        @param  freqTab :
        @param  limitTab :
        @return  :
        @author
        """
        pass

    def limitStatus(self, name = None, value = None):
        """


        @param string name :
        @param  value :
        @return  :
        @author
        """
        pass

    def limitCheck(self, name = None):
        """


        @param string name :
        @return  :
        @author
        """
        pass

    def screenShot(self, name = None):
        """


        @param string name :
        @return  :
        @author
        """
        pass

    def freqStart(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def freqCenter(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def freqStop(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def freqSpan(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def refLvl(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def refLvlOffset(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def inputAtt(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def rbw(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def vbw(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def sweep(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def averageCount(self, value = None):
        """


        @param int value :
        @return  :
        @author
        """
        pass

    def statAverage(self, value = None):
        """


        @param bool value :
        @return  :
        @author
        """
        pass

    def statSweep(self, value = None):
        """


        @param bool value :
        @return  :
        @author
        """
        pass

    def markPeakSearch(self):
        """


        @return  :
        @author
        """
        pass

    def markSet(self, number = 1, freq = None, status = True):
        """


        @param int number :
        @param int freq :
        @param bool status :
        @return  :
        @author
        """
        pass

    def markSearchLimit(self, number = 1, dir = None, freq = None, status = True):
        """


        @param int number :
        @param string dir :
        @param int freq :
        @param bool status :
        @return  :
        @author
        """
        pass

    def markGet(self, number = 1):
        """


        @param int number :
        @return  :
        @author
        """
        pass

    def markDelta(self, number = 1, mode = None, status = True):
        """


        @param int number :
        @param string mode :
        @param bool status :
        @return  :
        @author
        """
        pass

    def startSweep(self):
        """


        @return  :
        @author
        """
        pass

    def display(self, mode = None):
        """


        @param string mode :
        @return  :
        @author
        """
        pass

    def displayRefresh(self):
        """


        @return  :
        @author
        """
        pass

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
