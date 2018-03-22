# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from telnetlib import Telnet

class SpecAn(object):
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
        self.SpecAnConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.logger.info("Init SpecAn")
            try :
                self.inst = Telnet(self.SpecAnConf["ip"], 5025, 1)
                self._readWrite("SYST:PRES")
                self._readWrite("SYST:DISP:UPD ON")
            except :
                raise AcbbsError("RFSigGen Connection error: {0}".format(self.SpecAnConf["ip"]), log = self.logger)
        else :
            self.logger.info("Init RFSigGen in Simulate")
            self.inst = self._simulate()

        self.reference_var = None
        self.version_var = None

    def __del__(self):
        self.logger.info("Radio off")
        self.status = 0

    @property
    def info(self):
        return {
            "reference":self.reference,
            "version":self.version,
            "error":self.errors
        }

    def reset(self):
        self._readWrite("SYST:PRES")
        # self._readWrite("*CLS")
        # self._readWrite("*RST")

    @property
    def version(self):
        if self.version_var is None:
            if not self.simulate:
                self.version_var = self._readWrite("SYST:VERS?")
            else:
                self.version_var = "xxxx"
        return self.version_var

    @property
    def reference(self):
        if self.reference_var is None:
            if not self.simulate:
                self.reference_var = "xxxx"
            else:
                self.reference_var = "xxxx"
        return self.reference_var

    @property
    def errors(self):
        if not self.simulate:
            err = ""
            errList = []
            while "No error" not in err:
                err = self._readWrite("SYST:ERR?")
                if "No error" not in err:
                    errList.append(err)
                    self.logger.debug("read error %s" % err)
            return errList

        else:
            return []

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

    @property
    def freqStart(self):
        if not self.simulate:
            return self._readWrite("FREQ:START?")
        else:
            return "xxxx"

    @freqStart.setter
    def freqStart(self, value):
        if not self.simulate:
            return self._readWrite("FREQ:START", value)
        else:
            return "xxxx"

    @property
    def freqCenter(self, value = None):
        if not self.simulate:
            return self._readWrite("FREQ:CENT?")
        else:
            return "xxxx"

    @freqCenter.setter
    def freqCenter(self, value):
        self._readWrite("FREQ:CENT", value)

    @property
    def freqStop(self):
        if not self.simulate:
            return self._readWrite("FREQ:STOP?")
        else:
            return "xxxx"

    @freqStop.setter
    def freqStop(self, value):
        if not self.simulate:
            return self._readWrite("FREQ:STOP", value)
        else:
            return "xxxx"

    @property
    def freqSpan(self):
        if not self.simulate:
            return self._readWrite("FREQ:SPAN?")
        else:
            return "xxxx"

    @freqSpan.setter
    def freqSpan(self, value):
        if not self.simulate:
            return self._readWrite("FREQ:SPAN", value)
        else:
            return "xxxx"

    @property
    def refLvl(self):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEVel?")
        else:
            return "xxxx"

    @refLvl.setter
    def refLvl(self, value):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEVel", value)
        else:
            return "xxxx"

    @property
    def refLvlOffset(self):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEV:OFFS?")
        else:
            return "xxxx"

    @refLvlOffset.setter
    def refLvlOffset(self, value):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEV:OFFS", value)
        else:
            return "xxxx"

    @property
    def inputAtten(self):
        if not self.simulate:
            return self._readWrite("INP:ATT?")
        else:
            return "xxxx"

    @inputAtten.setter
    def inputAtten(self, value):
        if not self.simulate:
            return self._readWrite("INP:ATT", value)
        else:
            return "xxxx"

    @property
    def rbw(self):
        if not self.simulate:
            return self._readWrite("SENS:BWID:RES?")
        else:
            return "xxxx"

    @rbw.setter
    def rbw(self, value):
        if not self.simulate:
            return self._readWrite("SENS:BWID:RES", value)
        else:
            return "xxxx"

    @property
    def vbw(self):
        if not self.simulate:
            return self._readWrite("SENS:BWID:VID?")
        else:
            return "xxxx"

    @vbw.setter
    def vbw(self, value):
        if not self.simulate:
            return self._readWrite("SENS:BWID:VID", value)
        else:
            return "xxxx"

    @property
    def sweep(self):
        if not self.simulate:
            return self._readWrite("SENS:SWE:TIME?")
        else:
            return "xxxx"

    @sweep.setter
    def sweep(self, value):
        if not self.simulate:
            return self._readWrite("SENS:SWE:TIME", value)
        else:
            return "xxxx"

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

    def sweepCount(self, value):
        self._readWrite("INIT:CONT OFF")
        self._readWrite("AVER:COUN", value)
        self._readWrite("INIT;*WAI")

    def markPeakSearch(self):
        self._readWrite("CALC:MARK:MAX")
        return float(self._readWrite("CALC:MARK1:Y?"))

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


    def _wait(self):
        self.inst.write("*WAI\n")
        return

    def _readWrite(self, cmd = None, value = None):
        self.logger.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write("%s\n" % cmd)
            return(self.inst.read_until("\n")[:-1])
        elif value is None:
            self.inst.write("%s\n" % (cmd))
            self._wait()
        else:
            self.inst.write("%s %s\n" % (cmd, value))
            self._wait()

        err = self.errors
        if len(err) != 0:
            strerr = ""
            for e in err:
                strerr += "|%s| " % e
            if value is None:
                c = "%s" % (cmd.split("\n")[0])
            else:
                c = "%s %s" % (cmd.split("\n")[0], value)
            self.logger.warning("Get following errors after \"{0}\" command : {1}".format(c, strerr))
