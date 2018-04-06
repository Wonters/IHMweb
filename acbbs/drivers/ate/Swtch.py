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
        if sw1 is not None:
            self.channel = sw1
        if not self.simulate:
            #configure switch
            self.__connect()
            self.tn.write("S\r\n")
            ret = self.tn.read_until("\r\n")
            if sw1 is None:
                sw1 = int(ret[1])
            if sw2 is None:
                sw2 = int(ret[2])
            if sw3 is None:
                sw3 = int(ret[3])
            if sw4 is None:
                sw4 = int(ret[4])
            self.tn.write('c' + str(sw1) + str(sw2) + str(sw3) + str(sw4) + '\r\n')
            ret = self.tn.read_until("\r\n")
            self.__disconnect()

        else:
            if sw1 is None:
                sw1 = 1
            if sw2 is None:
                sw2 = 4
            if sw3 is None:
                sw3 = 3
            if sw4 is None:
                sw4 = 1

        #return correct offset depending of switch configurationFile

        if sw3 == 2:
            return {"noise-soure":self.swtchConf["loss"]["J{0}-J18".format(sw1+8)]}
        elif sw3 == 3 and sw4 == 1:
            return {"pwr-meter":self.swtchConf["loss"]["J{0}-J2".format(sw1+8)],
                    "fsv-fswr":self.swtchConf["loss"]["J{0}-J5".format(sw1+8)],
                    "smb100a":self.swtchConf["loss"]["J{0}-J4_20dB".format(sw1+8)]}
        elif sw3 == 3 and sw4 == 2:
            return {"pwr-meter":self.swtchConf["loss"]["J{0}-J2".format(sw1+8)],
                    "fsv-fswr":self.swtchConf["loss"]["J{0}-J5".format(sw1+8)]}
        elif sw3 == 4 and sw4 == 1:
            return {"smbv100a":self.swtchConf["loss"]["J{0}-J3".format(sw1+8)]}
        elif sw3 == 4 and sw4 == 2:
            return {"smbv100a":self.swtchConf["loss"]["J{0}-J3".format(sw1+8)],
                    "smb100a":self.swtchConf["loss"]["J{0}-J4".format(sw1+8)]}
        else:
            raise commutRackException()
