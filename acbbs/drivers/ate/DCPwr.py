# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from telnetlib import Telnet

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

        if not simulate:
            self.logger.info("New power instance")
            self.simulate = False
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
            self.simulate = True
            self.powerDevice1 = self._simulate()
            self.powerDevice2 = self._simulate()

        self.currentChan = None

    def reset(self):
        self._readWrite("*RST")

    @property
    def version(self):
        return self._readWrite("SYST:VERS?")

    @property
    def status(self):
        return self._readWrite("OUTP:STAT?")

    @status.setter
    def status(self, value):
        self.logger.info("Change status to %s" % value, ch = self.currentChan)
        self._readWrite("OUTP:STAT", value)

    @property
    def voltageConsigne(self):
        return self._readWrite("VOLT?")

    @property
    def voltageReal(self):
        return self._readWrite("MEAS:VOLT?")

    def voltage(self, value):
        self.logger.info("Change voltage to %s" % value, ch = self.currentChan)
        self._readWrite("VOLT", value)

    @property
    def currentConsigne(self):
        return self._readWrite("CURR?")

    @property
    def currentReal(self):
        return self._readWrite("MEAS:CURR?")

    def current(self, value):
        self.logger.info("Change current to %s" % value, ch = self.currentChan)
        self._readWrite("CURR", value)

    @property
    def errors(self):
        if not self.simulate:
            err = ""
            errList = []
            while "No error" not in err:
                err = self._readWrite("SYST:ERR?")
                if "No error" not in err:
                    errList.append(err)
                    self.logger.debug("read error %s" % err, ch = self.currentChan)
            return errList

        else:
            return []

    def selChan(self, channel):
        if int(channel) in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.logger.info("Change channel to %s" % channel, ch = self.currentChan)
            self.currentChan = channel
        else:
            raise AcbbsError("Bad Channel", ch = self.currentChan, log = self.logger)

    def _wait(self):
        if self.currentChan != None:
            if self.currentChan in [1, 2, 3, 4]:
                self.powerDevice1.write("*WAI\n")
                return
            elif self.currentChan in [5, 6, 7, 8]:
                self.powerDevice2.write("*WAI\n")
                return

        else:
            raise AcbbsError("Channel not set", log = self.logger)

    def _readWrite(self, cmd = None, value = None):
        if "?" in cmd:
            device = self._channelSel()
            device.write("%s\n" % cmd)
            return(device.read_until("\n")[:-1])
        else:
            self._channelSel().write("%s %s\n" % (cmd, value))
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
            self.logger.warning("Get following errors after \"{0}\" command : {1}".format(c, strerr), ch = self.currentChan)


    def _channelSel(self):
        if int(self.currentChan) in [1, 2, 3, 4]:
            self.powerDevice1.write("INST:NSEL?\n")
            if self.powerDevice1.read_until("\n")[:-1] != str(self.currentChan):
                self.logger.debug("Write on channel %s on powerDevice1" % self.currentChan, ch = self.currentChan)
                self.powerDevice1.write("INST:NSEL %s\n" % self.currentChan)
                self._wait()
            return self.powerDevice1
        elif int(self.currentChan) in [5, 6, 7, 8]:
            channel = (int(self.currentChan) - 4)
            self.powerDevice2.write("INST:NSEL?\n")
            if self.powerDevice2.read_until("\n")[:-1] != str(channel):
                self.logger.debug("Write on channel %s on powerDevice2" % channel, ch = self.currentChan)
                self.powerDevice2.write("INST:NSEL %s\n" % int(channel))
                self._wait()
            return self.powerDevice2
        else:
            raise AcbbsError("Bad Channel", ch = self.currentChan, log = self.logger)
