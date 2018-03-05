# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

class DCPwr(object):
    '''
    This class is the driver for the hmp4040 power
    '''
    class _simulate(object):
        def __init__(self):
            return
        def write(self, val):
            return '0'
        def read_until(self, val, timeout=None):
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
            try :
                self.powerDevice1 = Telnet(self.dcConf["self.powerDevice1-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 1 Connection error", log = self.logger)
            try :
                self.powerDevice2 = Telnet(self.dcConf["self.powerDevice2-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 2 Connection error", log = self.logger)
            self.powerDevice1.write("OUTP:GEN ON\n")
            self.powerDevice2.write("OUTP:GEN ON\n")
        else :
            self.logger.info("New power instance in Simulate")
            self.powerDevice1 = self._simulate()
            self.powerDevice2 = self._simulate()

        self.currentChan = None

    def getErrors(self):
        return []

    @property
    def reference(self):
        return ""

    @property
    def version(self):
        return ""

    @property
    def status(self):
        return ""

    @property
    def voltage(self):
        return self._readWrite("VOLT?")

    @voltage.setter
    def voltage(self, value):
        self.logger.info("Change voltage to %s" % voltage, ch = self.currentChan)
        self._readWrite("VOLT", voltage)

    @property
    def current(self):
        return self._readWrite("CURR?")

    @current.setter
    def current(self, value):
        self.logger.info("Change current to %s" % self.currentChan, ch = channel)
        self._readWrite("CURR", current)

    def selChan(self, channel):
        if int(channel) in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.currentChan = channel

        else:
            raise AcbbsError("Bad Channel", ch= self.currentChan, log=self.logger)

    def _wait(self):
        if self.currentChan != None:
            if self.currentChan in [1, 2, 3, 4]:
                self.powerDevice1.write("*WAI\n")
                return
            elif self.currentChan in [5, 6, 7, 8]:
                self.powerDevice2.write("*WAI\n")
                return

        else:
            raise AcbbsError("Channel not set", log=self.logger)

    def _readWrite(self, cmd = None, value = None):
        if "?" in cmd:
            device = self._channelSel()
            device.write("%s\n" % cmd)
            return(device.read_until("\n")[:-1])
        else:
            self._channelSel().write("%s %s\n" % (cmd, value))
            self._wait(self.currentChan)

    def _channelSel(self):
        if int(self.currentChan) in [1, 2, 3, 4]:
            self.powerDevice1.write("INST:NSEL?\n")
            if self.powerDevice1.read_until("\n")[:-1] != str(self.currentChan):
                self.powerDevice1.write("INST:NSEL %s\n" % self.currentChan)
                self._wait()
            return self.powerDevice1
        elif int(self.currentChan) in [5, 6, 7, 8]:
            channel = (int(self.currentChan) - 4)
            self.powerDevice2.write("INST:NSEL?\n")
            if self.powerDevice2.read_until("\n")[:-1] != str(self.currentChan):
                self.powerDevice2.write("INST:NSEL %s\n" % int(self.currentChan))
                self._wait(self.currentChan)
            return self.powerDevice2
        else:
            raise AcbbsError("Bad Channel", ch= self.currentChan, log=self.logger)
