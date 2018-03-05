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

    powerDevice1 = None
    powerDevice2 = None

    def __init__(self, simulate = False):
        """Constructor
        When called without arguments, create a connected instance with the device
        :param simulate: simulation for unity tests if it's True(1), simulation mode is activated
        :type simulate: bool
        """

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration dataBase
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dcConf = self.conf.getConfiguration()

        if not simulate:
            self.logger.info("New power instance")
            try :
                if Ps_hmp4040.powerDevice1 is None:
                    Ps_hmp4040.powerDevice1 = Telnet(self.dcConf["powerDevice1-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 1 Connection error", log = self.logger)
            try :
                if Ps_hmp4040.powerDevice2 is None:
                    Ps_hmp4040.powerDevice2 = Telnet(self.dcConf["powerDevice2-ip"], 5025, 1)
            except :
                raise AcbbsError("hmp4040 2 Connection error", log = self.logger)
            Ps_hmp4040.powerDevice1.write("OUTP:GEN ON\n")
            Ps_hmp4040.powerDevice2.write("OUTP:GEN ON\n")
        else :
            self.logger.info("New power instance in Simulate")
            DCPwr.powerDevice1 = self._simulate()

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
        return self._readWrite(channel, "VOLT?")

    @voltage.setter
    def voltage(self, value):
        self.logger.info("Change voltage to %s" % voltage, ch = self.currentChan)
        self._readWrite("VOLT", voltage)

    @property
    def current(self):
        return self._readWrite(channel, "CURR?")

    @current.setter
    def current(self, value):
        self.logger.info("Change current to %s" % self.currentChan, ch = channel)
        self._readWrite("CURR", current)

    def selChan(self, channel):
        if int(channel) in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.currentChan = channel

        else:
            raise AcbbsError("Bad Channel", ch= self.currentChan, log=self.logger)

    def __wait(self):
        if self.currentChan != None:
            if int(channel) in [1, 2, 3, 4]:
                Ps_hmp4040.powerDevice1.write("*WAI\n")
                return
            elif int(channel) in [5, 6, 7, 8]:
                Ps_hmp4040.powerDevice2.write("*WAI\n")
                return

        else:
            raise AcbbsError("Channel not set", log=self.logger)

    def __readWrite(self, cmd = None, value = None):
        if "?" in cmd:
            device = self._channelSel()
            device.write("%s\n" % cmd)
            return(device.read_until("\n")[:-1])
        else:
            self._channelSel().write("%s %s\n" % (cmd, value))
            self._wait(self.currentChan)

    def __channelSel(self):
        if int(self.currentChan) in [1, 2, 3, 4]:
            Ps_hmp4040.powerDevice1.write("INST:NSEL?\n")
            if Ps_hmp4040.powerDevice1.read_until("\n")[:-1] != str(self.currentChan):
                Ps_hmp4040.powerDevice1.write("INST:NSEL %s\n" % self.currentChan)
                self._wait(self.currentChan)
            return Ps_hmp4040.powerDevice1
        elif int(self.currentChan) in [5, 6, 7, 8]:
            channel = (int(self.currentChan) - 4)
            Ps_hmp4040.powerDevice2.write("INST:NSEL?\n")
            if Ps_hmp4040.powerDevice2.read_until("\n")[:-1] != str(self.currentChan):
                Ps_hmp4040.powerDevice2.write("INST:NSEL %s\n" % int(self.currentChan))
                self._wait(self.currentChan)
            return Ps_hmp4040.powerDevice2
        else:
            raise AcbbsError("Bad Channel", ch= self.currentChan, log=self.logger)
