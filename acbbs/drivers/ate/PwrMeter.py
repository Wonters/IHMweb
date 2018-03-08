# coding=UTF-8
from acbbs.tools.log import *

class PwrMeter(object):
    def __init__(self, simulate = False):
        if not simulate:
            self.simulate = False

        else:
            self.simulate = True

    @property
    def errors(self):
        if not self.simulate:
            return []

        else:
            return []

    @property
    def reference(self):
        return ""

    @property
    def version(self):
        return ""

    def reset(self):
        """


        @return  :
        @author
        """
        pass

    def measure(self, freq = 1000000000, trigMode = "SLOP POS", trigState = "OFF", avgVal = 1, avgState = "ON", pmCh = 1):
        """


        @param int freq :
        @param string trigMode :
        @param string trigState :
        @param int avgVal :
        @param string avgState :
        @param  pmCh :
        @return  :
        @author
        """
        pass

    def identification(self, cmd = "*IDN?"):
        """


        @param string cmd :
        @return  :
        @author
        """
        pass

    def calibrationZeroAuto(self, mode = None, pmCh = 1):
        """


        @param  mode :
        @param  pmCh :
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

    def __readWrite(self, cmd = None, value = None):
        """


        @param  cmd :
        @param  value :
        @return  :
        @author
        """
        pass

    def __frequency(self, freq = None, pmCh = 1):
        """


        @param int freq :
        @param  pmCh :
        @return  :
        @author
        """
        pass

    def __averageCount(self, average = None, state = "OFF", pmCh = 1):
        """


        @param  average :
        @param string state :
        @param  pmCh :
        @return  :
        @author
        """
        pass

    def __senseFunction(self, mode = "OFF", unit = "DBM", state = "OFF", pmCh = 1):
        """


        @param string mode :
        @param string unit :
        @param string state :
        @param  pmCh :
        @return  :
        @author
        """
        pass
