# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from telnetlib import Telnet

class RFSigGen(object):
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
        self.sigGenConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.logger.info("Init RFSigGen")
            try :
                self.inst = Telnet(self.sigGenConf["ip"], 5025, 1)
            except :
                raise AcbbsError("RFSigGen Connection error: {0}".format(self.sigGenConf["ip"]), log = self.logger)
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
    def status(self):
        if not self.simulate:
            return self._readWrite("OUTP:STAT?")
        else:
            return "xxxx"

    @status.setter
    def status(self, value):
        self.logger.info("Change status to %s" % value)
        self._readWrite("OUTP:STAT", value)

    @property
    def power(self):
        if not self.simulate:
            return self._readWrite("SOUR:POW:LEV:IMM:AMPL?")
        else:
            return "xxxx"

    @power.setter
    def power(self, value):
        self.logger.info("Change power to %s" % value)
        self._readWrite("SOUR:POW:LEV:IMM:AMPL", float(value) + float(self.sigGenConf["cableLoss"]))

    @property
    def freq(self):
        if not self.simulate:
            return self._readWrite("SOUR:FREQ:CW?")
        else:
            return "xxxx"

    @freq.setter
    def freq(self, value):
        self.logger.info("Change freq to %s" % value)
        self._readWrite("SOUR:FREQ:CW", value)

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
