# coding=UTF-8
from acbbs.tools.log import get_logger, AcbbsError
from acbbs.tools.configurationFile import configurationFile

from telnetlib import Telnet

TIMEOUT = 5

class RFSigGenCal(object):
    class _simulate(object):
        def __init__(self):
            return
        def write(self, val):
            return b'0'
        def read(self, val, timeout=None):
            return b'0'

    def __init__(self, simulate = False):

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration
        #self.conf = configurationFile(file = self.__class__.__name__)
        #self.sigGenVConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.logger.info("Init RFSigGenCal")
            try :
                self.inst = Telnet(self.sigGenVConf["ip"], 5025, 1)
            except :
                raise AcbbsError("RFSigGenCal Connection error: {0}".format(self.sigGenVConf["ip"]), log = self.logger)
        else :
            self.logger.info("Init RFSigGenCal in Simulate")
            self.inst = self._simulate()

        self.reference_var = None
        self.version_var = None

    def __del__(self):
        self.logger.info("Radio off")
        self.status = 0

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
                self.version_var = 0.0
        self.logger.debug("Get version : {}".format(self.version_var))
        return self.version_var

    @property
    def errors(self):
        # if not self.simulate:
        #     err = ""
        #     errList = []
        #     while "No error" not in err:
        #         err = self._readWrite("SYST:ERR?")
        #         if "No error" not in err:
        #             errList.append(err)
        #             self.logger.debug("read error %s" % err)
        #     return errList

        # else:
        return []

    @property
    def status(self):
        if not self.simulate:
            value = self._readWrite("OUTP:STAT?")
        else:
            value = 0.0
        self.logger.debug("Get status : {}".format(value))
        return value

    @status.setter
    def status(self, value):
        self.logger.debug("Set status : {}".format(value))
        self._readWrite("OUTP:STAT", value)

    @property
    def power(self):
        if not self.simulate:
            value = self._readWrite("SOUR:POW:LEV:IMM:AMPL?")
        else:
            value = 0.0
        self.logger.debug("Get power : {}".format(value))
        return value

    @power.setter
    def power(self, value):
        self.logger.debug("Set power : {}".format(value))
        self._readWrite("SOUR:POW:LEV:IMM:AMPL", float(value))

    @property
    def freq(self):
        if not self.simulate:
            value = self._readWrite("SOUR:FREQ:CW?")
        else:
            value = 0.0
        self.logger.debug("Get freq : {}".format(value))
        return value

    @freq.setter
    def freq(self, value):
        self.logger.debug("Set freq : {}".format(value))
        self._readWrite("SOUR:FREQ:CW", value)

    def _wait(self):
        self.inst.write(("*WAI\n").encode('ascii'))
        return

    def _readWrite(self, cmd = None, value = None):
        self.logger.debug("Write command : {0} with value : {1}".format(cmd, value))
        if "?" in cmd:
            self.inst.write(("%s\n" % cmd).encode('ascii'))
            out = (self.inst.read_until(("\n").encode('ascii'), timeout=TIMEOUT)).decode("utf-8")[:-1]
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