# coding=UTF-8
from ...tools.log import get_logger, AcbbsError
from ...tools.configurationFile import configurationFile

from telnetlib import Telnet

TIMEOUT = 5

class PwrMeter(object):
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
        self.PwrMeterConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.logger.info("Init PwrMeter")
            try :
                self.inst = Telnet(self.PwrMeterConf["ip"], 5025, 1)
                self._readWrite("SENS:PMET:STAT 1")
                self._readWrite("SENS:PMET:ROFF 0")
                self._readWrite("SENS:PMET:MTIM:AVER", self.PwrMeterConf["avrCount"])
            except :
                raise AcbbsError("PwrMeter Connection error: {0}".format(self.PwrMeterConf["ip"]), log = self.logger)
        else :
            self.logger.info("Init PwrMeter in Simulate")
            self.inst = self._simulate()

        self.reference_var = None
        self.version_var = None

    def __del__(self):
        self.logger.info("PwrMeter off")
        self._readWrite("SENS:PMET:STAT 0")

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
                self.version_var = 0.0
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
            return errList

        else:
            return []

    @property
    def status(self):
        return self._readWrite("SENS:PMET:STAT?")

    @property
    def freq(self, value = None):
        if not self.simulate:
            return self._readWrite("SENS:PMET:FREQ?")
        else:
            return 0.0

    @freq.setter
    def freq(self, value):
        self._readWrite("SENS:PMET:FREQ", value)

    @property
    def power(self):
        if self.simulate:
            return 0.0
        else:
            return(float(self._readWrite("READ:PMET?")))

    def _wait(self):
        self.inst.write("*WAI\n")
        return

    def _readWrite(self, cmd = None, value = None):
        self.logger.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write("%s\n" % cmd)
            out = self.inst.read_until("\n", timeout=TIMEOUT)[:-1]
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
