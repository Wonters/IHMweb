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
        def read_until(self, val):
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
                raise AcbbsError("SpecAn Connection error: {0}".format(self.SpecAnConf["ip"]), log = self.logger)
        else :
            self.logger.info("Init SpecAn in Simulate")
            self.inst = self._simulate()

        self.reference_var = None
        self.version_var = None

    @property
    def info(self):
        return {
            "version":self.version,
            "error":self.errors
        }

    def reset(self):
        self._readWrite("SYST:PRES")

    @property
    def version(self):
        if self.version_var is None:
            if not self.simulate:
                self.version_var = self._readWrite("SYST:VERS?")
            else:
                self.version_var = "xxxx"
        return self.version_var

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

    @property
    def freqStart(self):
        if not self.simulate:
            return self._readWrite("FREQ:START?")
        else:
            return 0.0

    @freqStart.setter
    def freqStart(self, value):
        return self._readWrite("FREQ:START", value)

    @property
    def freqCenter(self, value = None):
        if not self.simulate:
            return self._readWrite("FREQ:CENT?")
        else:
            return 0.0

    @freqCenter.setter
    def freqCenter(self, value):
        self._readWrite("FREQ:CENT", value)

    @property
    def freqStop(self):
        if not self.simulate:
            return self._readWrite("FREQ:STOP?")
        else:
            return 0.0

    @freqStop.setter
    def freqStop(self, value):
        return self._readWrite("FREQ:STOP", value)

    @property
    def freqSpan(self):
        if not self.simulate:
            return self._readWrite("FREQ:SPAN?")
        else:
            return 0.0

    @freqSpan.setter
    def freqSpan(self, value):
        return self._readWrite("FREQ:SPAN", value)

    @property
    def refLvl(self):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEVel?")
        else:
            return 0.0

    @refLvl.setter
    def refLvl(self, value):
        return self._readWrite("DISP:TRAC1:Y:RLEVel", value)

    @property
    def refLvlOffset(self):
        if not self.simulate:
            return self._readWrite("DISP:TRAC1:Y:RLEV:OFFS?")
        else:
            return 0.0

    @refLvlOffset.setter
    def refLvlOffset(self, value):
        return self._readWrite("DISP:TRAC1:Y:RLEV:OFFS", value)

    @property
    def inputAtten(self):
        if not self.simulate:
            return self._readWrite("INP:ATT?")
        else:
            return 0.0

    @inputAtten.setter
    def inputAtten(self, value):
        return self._readWrite("INP:ATT", value)

    @property
    def rbw(self):
        if not self.simulate:
            return self._readWrite("SENS:BWID:RES?")
        else:
            return 0.0

    @rbw.setter
    def rbw(self, value):
        return self._readWrite("SENS:BWID:RES", value)

    @property
    def vbw(self):
        if not self.simulate:
            return self._readWrite("SENS:BWID:VID?")
        else:
            return 0.0

    @vbw.setter
    def vbw(self, value):
        return self._readWrite("SENS:BWID:VID", value)

    @property
    def sweep(self):
        if not self.simulate:
            return self._readWrite("SENS:SWE:TIME?")
        else:
            return 0.0

    @sweep.setter
    def sweep(self, value):
        return self._readWrite("SENS:SWE:TIME", value)

    def refreshDisplay(self):
        self._readWrite("INIT:CONT OFF")
        self._readWrite("DISP:TRAC:MODE WRIT")
        self._readWrite("INIT:CONT ON")

    def averageCount(self, value):
        self._readWrite("INIT:CONT OFF")
        self._readWrite("AVER:COUN", value)
        self._readWrite("INIT;*WAI")

    def maxHoldCount(self, value):
        self._readWrite("INIT:CONT OFF")
        self._readWrite("SWE:COUN", value)
        self._readWrite("DISP:TRAC:MODE MAXH")
        self._readWrite("INIT;*WAI")

    def markerPeakSearch(self, marker = 1):
        if self.simulate:
            return [0.0, 0.0]
        else:
            self._readWrite("CALC:MARK{0}:MAX".format(marker))
            return [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]

    def markerSearch(self, marker = 1, dir = None):
        if dir == 'r':
            self._readWrite("CALC:MARK{0}:MAX:RIGH".format(marker))
        if dir == 'l':
            self._readWrite("CALC:MARK{0}:MAX:LEFT".format(marker))
        if dir == 'n':
            self._readWrite("CALC:MARK{0}:MAX:NEXT".format(marker))
        return [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]

    def markerSet(self, marker = 1, freq = None, status = 1):
        if freq is not None:
            self._readWrite("CALC:MARK{0}:X".format(marker), freq)
        self._readWrite("CALC:MARK{0}".format(marker), status)

    def markerGet(self, marker = 1):
        return [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]

    def markerSearchLimit(self, marker = 1, freqleft = None, freqright = None, status = 1):
        if not self.simulate:
            if freqleft is not None and freqright is not None:
                self._readWrite("CALC:MARK{0}:X:SLIM:LEFT".format(marker), freqleft)
                self._readWrite("CALC:MARK{0}:X:SLIM:RIGHT".format(marker), freqright)

            self._readWrite("CALC:MARK{0}:X:SLIM".format(marker), status)


    def markerDelta(self, marker = 1, mode = None, delta = None, status = 1):
        if self.simulate:
            return 0.0
        else:
            if mode is not None and delta is not None:
                self._readWrite("CALC:DELT{0}:MODE".format(marker), mode)
                self._readWrite("CALC:DELT{0}:X".format(marker), delta)

            self._readWrite("CALC:DELT{0}".format(marker), status)

            return float(self._readWrite("CALC:DELT{0}:Y?".format(marker)))

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

    def limitLineHSet(self, line = 1, power = None, status = None):
        if status is not None:
            self._readWrite("CALC:DLIN{0}:STAT".format(line), status)
        else:
            self._readWrite("CALC:DLIN{0}:STAT ON".format(line))
            self._readWrite("CALC:DLIN{0}".format(line), power)

    def limitLineVSet(self, line = 1, freq = None, status = None):
        if status is not None:
            self._readWrite("CALC:FLIN{0}:STAT".format(line), status)
        else:
            self._readWrite("CALC:FLIN{0}:STAT ON".format(line))
            self._readWrite("CALC:FLIN{0}".format(line), freq)

    def limitSet(self, limit = 1, freq = None, power = None, margin = 0):
        if len(freq) != len(power):
            raise AcbbsError("freq and power not same size", log = self.logger)

        freqString = ""
        for i in range (0, len(freq)-1):
            freqString += str(freq[i]) + ","
        freqString += str(freq[len(freq)-1])

        powerString = ""
        for i in range (0, len(power)-1):
            powerString += str(power[i]) + ","
        powerString += str(power[len(power)-1])

        self._readWrite("CALC:LIM{0}:CONT:MODE ABS".format(limit))
        self._readWrite("CALC:LIM{0}:UPP:MODE ABS".format(limit))
        self._readWrite("CALC:LIM{0}:UNIT DBM".format(limit))
        self._readWrite("CALC:LIM{0}:CONT".format(limit), freqString)
        self._readWrite("CALC:LIM{0}:UPP".format(limit), powerString)
        self._readWrite("CALC:LIM{0}:UPP:MARG".format(limit), margin)
        self._readWrite("CALC:LIM{0}:STAT ON".format(limit))

    def limitState(self, limit = 1, status = None):
        self._readWrite("CALC:LIM{0}:STAT".format(limit), status)

    def limitCheck(self, limit = 1):
        return self._readWrite("CALC:LIM{0}:FAIL?".format(limit))

    def _wait(self):
        self.inst.write("*WAI\n")
        return

    def _readWrite(self, cmd = None, value = None):
        self.logger.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write("%s\n" % cmd)
            out = self.inst.read_until("\n")[:-1]
            try:
                return float(out)
            except:
                return out
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
