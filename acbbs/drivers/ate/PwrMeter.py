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
            return b'0'
        def read(self, val, timeout=None):
            return b'0'
        def read_until(self, val, timeout=None):
            return b'0'

    def __init__(self, simulate = False):

        #init logs
        self.log = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.PwrMeterConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.log.info("Init PwrMeter")
            try :
                self.inst = Telnet(self.PwrMeterConf["ip"], 5025, 1)
                self._readWrite("SENS:PMET:STAT 1")
                self._readWrite("SENS:PMET:ROFF 0")
                self._readWrite("SENS:PMET:MTIM:AVER", self.PwrMeterConf["avrCount"])
            except :
                raise AcbbsError("PwrMeter Connection error: {0}".format(self.PwrMeterConf["ip"]), log = self.log)
        else :
            self.log.info("Init PwrMeter in Simulate")
            self.inst = self._simulate()

        self.reference_var = None
        self.version_var = None

    def __del__(self):
        self.log.info("PwrMeter off")
        self._readWrite("SENS:PMET:STAT 0")

    @property
    def info(self):
        self.log.debug("Get info")
        return {
            "version":self.version,
            "error":self.errors
        }

    def reset(self):
        self.log.debug("Reset")
        self._readWrite("SYST:PRES")

    @property
    def version(self):
        if self.version_var is None:
            if not self.simulate:
                self.version_var = self._readWrite("SYST:VERS?")
            else:
                self.version_var = 0.0
        self.log.debug("Get version : {}".format(self.version_var))
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
                    raise AcbbsError("read error %s" % err, log = self.log)
            return errList

        else:
            return []

    @property
    def status(self):
        if not self.simulate:
            value = self._readWrite("SENS:PMET:STAT?")
        else:
            value = 0.0
        self.log.debug("Get status : {}".format(value))
        return value

    @property
    def freq(self, value = None):
        if not self.simulate:
            value = self._readWrite("SENS:PMET:FREQ?")
        else:
            value = 0.0
        self.log.debug("Get freq : {}".format(value))
        return value

    @freq.setter
    def freq(self, value):
        self.log.debug("Set freq : {}".format(value))
        self._readWrite("SENS:PMET:FREQ", value)

    @property
    def power(self):
        if self.simulate:
            value = 0.0
        else:
            value = (self._readWrite("READ:PMET?"))
        self.log.debug("Get power : {}".format(value))
        return value

    def _wait(self):
        self.inst.write(("*WAI\n").encode('ascii'))
        return

    def _readWrite(self, cmd = None, value = None):
        self.log.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write(("%s\n" % cmd).encode('ascii'))
            out = (self.inst.read_until(("\n").encode('ascii'), timeout=TIMEOUT)).decode("utf-8")[:-1]
            self.log.debug("out : {0}".format(out))
            try:
                return float(out)
            except:
                return str(out)
        elif value is None:
            self.inst.write(("%s\n" % (cmd)).encode('ascii'))
            self._wait()
        else:
            self.inst.write(("%s %s\n" % (cmd, value)).encode('ascii'))
            self._wait()
