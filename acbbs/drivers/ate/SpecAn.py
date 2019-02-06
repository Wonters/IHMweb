# coding=UTF-8
from ...tools.log import get_logger, AcbbsError
from ...tools.configurationFile import configurationFile

from telnetlib import Telnet

TIMEOUT = 5

class SpecAn(object):
    class _simulate(object):
        def __init__(self):
            return
        def write(self, val):
            return '0'
        def read(self, val, timeout=None):
            return '0'
        def read_until(self, val, timeout=None):
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
        self.logger.debug("Get info")
        return {
            "version":self.version,
            "error":self.errors
        }

    def reset(self):
        self.logger.debug("Reset")
        self._readWrite("SYST:PRES")

    @property
    def version(self):
        if self.version_var is None:
            if not self.simulate:
                self.version_var = self._readWrite("SYST:VERS?")
            else:
                self.version_var = "xxxx"
        self.logger.debug("Get version : {}".format(self.version_var))
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
                    raise AcbbsError("read error %s" % err, log = self.logger)
            value = errList

        else:
            value = []
        self.logger.debug("Get errors : {}".format(value))
        return value

    @property
    def freqStart(self):
        if not self.simulate: 
            value = self._readWrite("FREQ:START?")
        else:
            value = 0.0
        self.logger.debug("Get Freq Start: {}".format(value))
        return value

    @freqStart.setter
    def freqStart(self, value):
        self.logger.debug("Set Freq Start: {}".format(value))
        return self._readWrite("FREQ:START", value)

    @property
    def freqCenter(self, value = None):
        if not self.simulate:
            value = self._readWrite("FREQ:CENT?")
        else:
            value =  0.0
        self.logger.debug("Set Freq Center : {}".format(value))
        return value

    @freqCenter.setter
    def freqCenter(self, value):
        self.logger.debug("Get Freq Center : {}".format(value))
        return self._readWrite("FREQ:CENT", value)

    @property
    def freqStop(self):
        if not self.simulate:
            value = self._readWrite("FREQ:STOP?")
        else:
            value = 0.0
        self.logger.debug("Get Freq Stop : {}".format(value))
        return value

    @freqStop.setter
    def freqStop(self, value):
        self.logger.debug("Set Freq Stop : {}".format(value))
        return self._readWrite("FREQ:STOP", value)

    @property
    def freqSpan(self):
        if not self.simulate:
            value = self._readWrite("FREQ:SPAN?")
        else:
            value = 0.0
        self.logger.debug("Get Freq Span : {}".format(value))
        return value

    @freqSpan.setter
    def freqSpan(self, value):
        self.logger.debug("Set Freq Span : {}".format(value))
        return self._readWrite("FREQ:SPAN", value)

    @property
    def refLvl(self):
        if not self.simulate:
            value = self._readWrite("DISP:TRAC1:Y:RLEVel?")
        else:
            value = 0.0
        self.logger.debug("Get Ref Lvl : {}".format(value))
        return value

    @refLvl.setter
    def refLvl(self, value):
        self.logger.debug("Set Ref Lvl : {}".format(value))
        return self._readWrite("DISP:TRAC1:Y:RLEVel", value)

    @property
    def refLvlOffset(self):
        if not self.simulate:
            value = self._readWrite("DISP:TRAC1:Y:RLEV:OFFS?")
        else:
            value = 0.0
        self.logger.debug("Get Ref Lvl Offset : {}".format(value))
        return value

    @refLvlOffset.setter
    def refLvlOffset(self, value):
        self.logger.debug("Set Ref Lvl Offset : {}".format(value))
        return self._readWrite("DISP:TRAC1:Y:RLEV:OFFS", value)

    @property
    def inputAtten(self):
        if not self.simulate:
            value = self._readWrite("INP:ATT?")
        else:
            value = 0.0
        self.logger.debug("Get Input Atten: {}".format(value))
        return value

    @inputAtten.setter
    def inputAtten(self, value):
        self.logger.debug("Set Input Atten : {}".format(value))
        return self._readWrite("INP:ATT", value)

    @property
    def rbw(self):
        if not self.simulate:
            value = self._readWrite("SENS:BWID:RES?")
        else:
            value = 0.0
        self.logger.debug("Get RBW : {}".format(value))
        return value

    @rbw.setter
    def rbw(self, value):
        self.logger.debug("Set RBW : {}".format(value))
        return self._readWrite("SENS:BWID:RES", value)

    @property
    def vbw(self):
        if not self.simulate:
            value = self._readWrite("SENS:BWID:VID?")
        else:
            value = 0.0
        self.logger.debug("Get VBW : {}".format(value))
        return value

    @vbw.setter
    def vbw(self, value):
        self.logger.debug("Set VBW : {}".format(value))
        return self._readWrite("SENS:BWID:VID", value)

    @property
    def sweep(self):
        if not self.simulate:
            value = self._readWrite("SENS:SWE:TIME?")
        else:
            value = 0.0
        self.logger.debug("Get Sweep : {}".format(value))
        return value

    @sweep.setter
    def sweep(self, value):
        self.logger.debug("Set Sweep : {}".format(value))
        return self._readWrite("SENS:SWE:TIME", value)

    def refreshDisplay(self):
        self.logger.debug("Refresh Display")
        self._readWrite("INIT:CONT OFF")
        self._readWrite("DISP:TRAC:MODE WRIT")
        self._readWrite("INIT:CONT ON")

    def averageCount(self, value):
        self.logger.debug("Average Count")
        self._readWrite("DISP:TRAC:MODE AVER")
        self._readWrite("INIT:CONT OFF")
        self._readWrite("AVER:COUN", value)
        self.runSingle()

    def maxHoldCount(self, value):
        self.logger.debug("Max Hold Count")
        self._readWrite("INIT:CONT OFF")
        self._readWrite("SWE:COUN", value)
        self._readWrite("DISP:TRAC:MODE MAXH")

    def runSingle(self):
        self.logger.debug("Run Single")
        self._readWrite("INIT;*WAI")

    def markerPeakSearch(self, marker = 1):
        if self.simulate:
            value = [0.0, 0.0]
        else:
            self._readWrite("CALC:MARK{0}:MAX".format(marker))
            value [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]
        self.logger.debug("Get Marker peak at marker {} : {}".format(marker, value))
        return value

    def markerSearch(self, marker = 1, dir = None):
        if self.simulate:
            value = [0.0, 0.0]
        else:
            if dir == 'r':
                self._readWrite("CALC:MARK{0}:MAX:RIGH".format(marker))
            if dir == 'l':
                self._readWrite("CALC:MARK{0}:MAX:LEFT".format(marker))
            if dir == 'n':
                self._readWrite("CALC:MARK{0}:MAX:NEXT".format(marker))
            value = [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]
        self.logger.debug("Get Marker Search at marker {}, dir {} : {}".format(marker, dir, value))
        return value

    def markerSet(self, marker = 1, freq = None, status = 1):
        self.logger.debug("Set Marker {} at {}Hz. (Status = {})".format(marker, freq, status))
        if freq is not None:
            self._readWrite("CALC:MARK{0}:X".format(marker), freq)
        self._readWrite("CALC:MARK{0}".format(marker), status)

    def markerGet(self, marker = 1):
        if self.simulate:
            value = [0.0, 0.0]
        else:
            value = [float(self._readWrite("CALC:MARK{0}:X?".format(marker))), float(self._readWrite("CALC:MARK{0}:Y?".format(marker)))]
        self.logger.debug("Get Marker {} : {}".format(marker, value))
        return value

    def markerSearchLimit(self, marker = 1, freqleft = None, freqright = None, status = 1):
        self.logger.debug("Set limit at marker {} : freqleft = {}, freqright = {}. (status = {})".format(marker, freqleft, freqright, status))
        if not self.simulate:
            self._readWrite("CALC:MARK{0}:X:SLIM".format(marker), status)
            if freqleft is not None and freqright is not None:
                self._readWrite("CALC:MARK{0}:X:SLIM:LEFT".format(marker), freqleft)
                self._readWrite("CALC:MARK{0}:X:SLIM:RIGHT".format(marker), freqright)

    def markerDelta(self, marker = 1, mode = None, delta = None, status = 1):
        if self.simulate:
            value = 0.0
        else:
            self._readWrite("CALC:DELT{0}".format(marker), status)
            if mode is not None and delta is not None:
                self._readWrite("CALC:DELT{0}:MODE".format(marker), mode)
                self._readWrite("CALC:DELT{0}:X".format(marker), delta)

            value = float(self._readWrite("CALC:DELT{0}:Y?".format(marker)))
        self.logger.debug("Get Marker Delta at marker {}, mode {}, delta {} : {}".format(marker, mode, delta, value))

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
        self.logger.debug("Set horizontal limit line {} at {}dBm. (status = {})".format(line, power, status))
        if status is not None:
            self._readWrite("CALC:DLIN{0}:STAT".format(line), status)
        else:
            self._readWrite("CALC:DLIN{0}:STAT ON".format(line))
            self._readWrite("CALC:DLIN{0}".format(line), power)

    def limitLineVSet(self, line = 1, freq = None, status = None):
        self.logger.debug("Set vertical limit line {} at {}Hz. (status = {})".format(line, freq, status))
        if status is not None:
            self._readWrite("CALC:FLIN{0}:STAT".format(line), status)
        else:
            self._readWrite("CALC:FLIN{0}:STAT ON".format(line))
            self._readWrite("CALC:FLIN{0}".format(line), freq)

    def limitSet(self, limit = 1, freq = None, power = None, margin = 0):
        self.logger.debug("Set limit at {}dBm, {}Hz, margin : {}".format(power, freq, margin))
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
        self.logger.debug("Set limit state. (status = {})".format(status))
        self._readWrite("CALC:LIM{0}:STAT".format(limit), status)

    def limitCheck(self, limit = 1):
        value = self._readWrite("CALC:LIM{0}:FAIL?".format(limit))
        self.logger.debug("Get limit {} check : {}".format(limit, value))
        return value

    def _wait(self):
        self.inst.write("*WAI\n")
        return

    def _readWrite(self, cmd = None, value = None):
        self.logger.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write("%s\n" % cmd)
            out = self.inst.read_until("\n", timeout=TIMEOUT)[:-1]
            self.logger.debug("out : {0}".format(out))
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
