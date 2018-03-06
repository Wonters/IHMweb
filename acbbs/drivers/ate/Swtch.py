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

        #if simulate
        if not simulate:
    		self.tn = Telnet(self.dcConf["swtch-ip"], 23, 2)
    		self.tn.write('enable \r\n')
    		self.tn.read_until("(enable)#")

        else:
            self.tn = self._simulate()

    def __connect(self):
		self.tn.write('connect line 2 \r\n')
		result = self.tn.read_until("Connected to line 2.\r\n", 1)
		if "Connected" not in result:
			raise commutRackException(result)
		self.tn.read_until("\r\n")

    def __disconnect(self):
		self.tn.write(chr(12))
		self.tn.read_until("#", 1)

    def setSwitch(self, sw1, sw2, sw3, sw4):
		self.__connect()
		self.tn.write("S\r\n")
		ret = self.tn.read_until("\r\n")

		self.tn.write('c' + str(sw1) + ret[2] + ret[3] + ret[4] + '\r\n')
		ret = self.tn.read_until("\r\n")

		self.tn.write('c' + ret[1] + str(sw2) + ret[3] + ret[4] + '\r\n')
		ret = self.tn.read_until("\r\n")

		self.tn.write('c' + ret[1] + ret[2] + str(sw3) + ret[4] + '\r\n')
		ret = self.tn.read_until("\r\n")

		self.tn.write('c' + ret[1] + ret[2] + ret[3] + str(sw4) + '\r\n')
		ret = self.tn.read_until("\r\n")

		self.__disconnect()
		return ret

    def getErrors(self):
        return []

    @property
    def reference(self):
        return ""

    @property
    def version(self):
        return ""
