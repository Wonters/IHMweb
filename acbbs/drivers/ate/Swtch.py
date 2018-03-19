# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from telnetlib import Telnet

class commutRackException(Exception):
    em = {0:  "No error"}

    def __init__(self, err = None, note = None):
        self.err = err
        self.note = note
        self.msg = ''

        if err is None:
            self.msg = note
        else:
            if type(err) is int:
                if err in self.em:
                    self.msg = "%d: %s" % (err, self.em[err])
                else:
                    self.msg = "%d: Unknown error" % err
            else:
                self.msg = err
            if note is not None:
                self.msg = "%s [%s]" % (self.msg, note)

    def __str__(self):
        return self.msg

class Swtch(object):
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
        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.swtchConf = self.conf.getConfiguration()

        #channel
        self.channel = 'N'

        #simulation state
        self.simulate = simulate

        #if simulate
        if not simulate:
            self.tn = Telnet(self.swtchConf["ip"], 23, 2)
            self.tn.write('enable \r\n')
            self.tn.read_until("(enable)#")

        else:
            self.tn = self._simulate()

    def __connect(self):
        if not self.simulate:
            self.tn.write('connect line 2 \r\n')
            result = self.tn.read_until("Connected to line 2.\r\n", 1)
            if "Connected" not in result:
                raise commutRackException(result)
                self.tn.read_until("\r\n")

    def __disconnect(self):
		self.tn.write(chr(12))
		self.tn.read_until("#", 1)

    def setSwitch(self, sw1 = None, sw2 = None, sw3 = None, sw4 = None):
        if not self.simulate:
            if sw1 is not None:
                self.channel = sw1
            if sw1 is not None:
                self.__connect()
                self.tn.write("S\r\n")
                ret = self.tn.read_until("\r\n")
                self.tn.write('c' + str(sw1) + ret[2] + ret[3] + ret[4] + '\r\n')
                ret = self.tn.read_until("\r\n")
                self.__disconnect()

            if sw2 is not None:
                self.__connect()
                self.tn.write("S\r\n")
                ret = self.tn.read_until("\r\n")
                self.tn.write('c' + ret[1] + str(sw2) + ret[3] + ret[4] + '\r\n')
                ret = self.tn.read_until("\r\n")
                self.__disconnect()

            if sw3 is not None:
                self.__connect()
                self.tn.write("S\r\n")
                ret = self.tn.read_until("\r\n")
                self.tn.write('c' + ret[1] + ret[2] + str(sw3) + ret[4] + '\r\n')
                ret = self.tn.read_until("\r\n")
                self.__disconnect()

            if sw4 is not None:
                self.__connect()
                self.tn.write("S\r\n")
                ret = self.tn.read_until("\r\n")
                self.tn.write('c' + ret[1] + ret[2] + ret[3] + str(sw4) + '\r\n')
                ret = self.tn.read_until("\r\n")
                self.__disconnect()

                self.__disconnect()
                return ret
        else:
            if sw1 is not None:
                self.channel = sw1
        return None
