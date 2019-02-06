# coding=UTF-8
from ...tools.log import get_logger, AcbbsError
from ...tools.configurationFile import configurationFile

from telnetlib import Telnet

TIMEOUT = 5

class DCPwr(object):
    '''
    This class is the driver for the hmp4040 power
    '''
    class _simulate(object):
        def __init__(self):
            return
        def write(self, val):
            return '0'
        def read_until(self, val, timeout = None):
            return '0'

    def __init__(self, simulate = False):
        """Constructor
        When called without arguments, create a connected instance with the device
        :param simulate: simulation for unity tests if it's True(1), simulation mode is activated
        :type simulate: bool
        """

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dcConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        #channel
        self.channel = 'N'

        if not simulate:
            self.logger.info("New power instance")
            try :
                self.powerDevice1 = Telnet(self.dcConf["powerDevice1-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 1 Connection error: {0}".format(self.dcConf["powerDevice2-ip"]), log = self.logger)
            try :
                self.powerDevice2 = Telnet(self.dcConf["powerDevice2-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 2 Connection error : {0}".format(self.dcConf["powerDevice2-ip"]), log = self.logger)
            self.powerDevice1.write("OUTP:GEN ON\n")
            self.powerDevice2.write("OUTP:GEN ON\n")
        else:
            self.logger.info("New power instance in Simulate")
            self.powerDevice1 = self._simulate()
            self.powerDevice2 = self._simulate()

        self.version_var = None

    @property
    def info(self):
        self.logger.debug("Get info")
        return {
            "version":self.version,
            "error":self.errors,
            "status":self.status,
            "Power_Supply_Max_Current_(A)":self.currentConsigne,
            "Power_Supply_Current_(A)":self.currentReal,
            "Power_Supply_Prog_Voltage_(V)":self.voltageConsigne,
            "Power_Supply_Voltage_(V)":self.voltageReal
        }

    def reset(self):
        self.logger.debug("Reset")
        self._readWrite("*RST")

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
    def status(self):
        if not self.simulate:
            value = self._readWrite("OUTP:STAT?")
        else:
            value = 0.0
        self.logger.debug("Get status : {}".format(value), ch = self.channel)
        return value

    @status.setter
    def status(self, value):
        self.logger.debug("Set status : {}".format(value), ch = self.channel)
        self._readWrite("OUTP:STAT", value)

    @property
    def voltageConsigne(self):
        if not self.simulate:
            value = self._readWrite("VOLT?")
        else:
            value = 0.0
        self.logger.debug("Get voltageConsigne : {}".format(value), ch = self.channel)
        return value

    @property
    def voltageReal(self):
        if not self.simulate:
            value = self._readWrite("MEAS:VOLT?")
        else:
            value = 0.0

    @property
    def voltage(self):
        raise AcbbsError("Command not implemented", log = self.logger)

    @voltage.setter
    def voltage(self, value):
        self.logger.info("Change voltage to %s" % value, ch = self.channel)
        self._readWrite("VOLT", value)

    @property
    def currentConsigne(self):
        if not self.simulate:
            return self._readWrite("CURR?")
        else:
            return 0.0

    @property
    def currentReal(self):
        if not self.simulate:
            return self._readWrite("MEAS:CURR?")
        else:
            return 0.0

    @property
    def current(self):
        raise AcbbsError("Command not implemented", log = self.logger)

    @current.setter
    def current(self, value):
        self.logger.info("Change current to %s" % value, ch = self.channel)
        self._readWrite("CURR", value)

    @property
    def errors(self):
        # if not self.simulate:
        #     err = ""
        #     errList = []
        #     while "No error" not in err:
        #         err = self._readWrite("SYST:ERR?")
        #         if "No error" not in err:
        #             errList.append(err)
        #             self.logger.debug("read error %s" % err, ch = self.channel)
        #     return errList

        # else:
        return []

    def setChan(self, dutChan):
        if int(dutChan) in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.logger.info("Change channel to %s" % dutChan, ch = self.channel)
            self.channel = dutChan
        else:
            raise AcbbsError("Bad Channel", ch = self.channel, log = self.logger)

    def _wait(self):
        if self.channel != None:
            if self.channel in [1, 2, 3, 4]:
                self.powerDevice1.write("*WAI\n")
                return
            elif self.channel in [5, 6, 7, 8]:
                self.powerDevice2.write("*WAI\n")
                return

        else:
            raise AcbbsError("Channel not set", log = self.logger)

    def _readWrite(self, cmd = None, value = None):
        if "?" in cmd:
            device = self._channelSel()
            device.write("%s\n" % cmd)
            out = device.read_until("\n", timeout=TIMEOUT)[:-1]
            try:
                return float(out)
            except:
                return out
        else:
            self._channelSel().write("%s %s\n" % (cmd, int(value)))
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
            self.logger.warning("Get following errors after \"{0}\" command : {1}".format(c, strerr), ch = self.channel)


    def _channelSel(self):
        if int(self.channel) in [1, 2, 3, 4]:
            self.powerDevice1.write("INST:NSEL?\n")
            if self.powerDevice1.read_until("\n", timeout=TIMEOUT)[:-1] != str(self.channel):
                self.logger.debug("Write on channel %s on powerDevice1" % self.channel, ch = self.channel)
                self.powerDevice1.write("%s %s\n" % ("INST:NSEL", int(self.channel)))
                self._wait()
            return self.powerDevice1
        elif int(self.channel) in [5, 6, 7, 8]:
            channel = (int(self.channel) - 4)
            self.powerDevice2.write("INST:NSEL?\n")
            if self.powerDevice2.read_until("\n", timeout=TIMEOUT)[:-1] != str(channel):
                self.logger.debug("Write on channel %s on powerDevice2" % channel, ch = self.channel)
                self.powerDevice2.write("%s %s\n" % ("INST:NSEL", int(channel)))
                self._wait()
            return self.powerDevice2
        else:
            raise AcbbsError("Bad Channel", ch = self.channel, log = self.logger)
