# coding=UTF-8
from acbbs.tools.log import *

class PwrMeter(object):
    def __init__(self, simulate = False):

        #simulation state
        self.simulate = simulate

        if not simulate:
            pass
        else:
            pass

        self.reference_var = None
        self.version_var = None

    @property
    def info(self):
        return {
            "version":self.reference,
            "reference":self.version,
            "error":self.errors
        }

    @property
    def errors(self):
        if not self.simulate:
            return []

        else:
            return []

    @property
    def reference(self):
        if self.reference_var is None:
            if self.simulate:
                self.reference_var =  "xxxx"
            else:
                self.reference_var =  "xxxx"
        return self.reference_var

    @property
    def version(self):
        if self.version_var is None:
            if self.simulate:
                self.version_var =  "xxxx"
            else:
                self.version_var =  "xxxx"
        return self.version_var

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
