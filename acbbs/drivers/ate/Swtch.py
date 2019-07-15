# coding=UTF-8
from ...tools.log import get_logger
from ...tools.configurationFile import configurationFile

from telnetlib import Telnet

TIMEOUT = 5

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
        self.log = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.swtchConf = self.conf.getConfiguration()

        #channel
        self.channel = 'N'

        #simulation state
        self.simulate = simulate
        if self.simulate:
            self.sw1 = 1
            self.sw2 = 1
            self.sw3 = 1
            self.sw4 = 1

    def __connect(self):
        self.log.debug("Connect")
        if not self.simulate:
            self.tn = Telnet(self.swtchConf["ip"], 23, 2)
            self.tn.write(('enable \r\n').encode('ascii'))
            self.tn.read_until(("(enable)#").encode('ascii'))
            self.tn.write(('connect line 2 \r\n').encode('ascii'))
            result = (self.tn.read_until(("Connected to line 2.\r\n").encode('ascii'), 1)).decode("utf-8")
            if "Connected" not in result:
                raise commutRackException(result)
            self.tn.read_until(("\r\n").encode('ascii'))
        else:
            self.tn = self._simulate()

    def __disconnect(self):
        self.log.debug("Disconnect")
        self.tn.write((chr(12)).encode('ascii'))
        self.tn.read_until(("#").encode('ascii'), 1)
        self.tn.close()

    def setSwitch(self, sw1 = None, sw2 = None, sw3 = None, sw4 = None):
        self.log.debug("Set switch : {}, {}, {}, {}".format(sw1, sw2, sw3, sw4))
        if sw1 is not None:
            self.channel = sw1
        if not self.simulate:
            #configure switch
            self.__connect()
            self.tn.write(("S\r\n").encode('ascii'))
            ret = (self.tn.read_until(("\r\n").encode('ascii'))).decode("utf-8")
            if sw1 is None:
                sw1 = int(ret[1])
            if sw2 is None:
                sw2 = int(ret[2])
            if sw3 is None:
                sw3 = int(ret[3])
            if sw4 is None:
                sw4 = int(ret[4])
            self.tn.write(('c' + str(sw1) + str(sw2) + str(sw3) + str(sw4) + '\r\n').encode('ascii'))
            ret = (self.tn.read_until(("\r\n").encode('ascii'))).decode("utf-8")
            self.__disconnect()

        else:
            if sw1 is None:
                sw1 = self.sw1
            else:
                self.sw1 = sw1
            if sw2 is None:
                sw2 = self.sw2
            else:
                self.sw2 = sw2
            if sw3 is None:
                sw3 = self.sw3
            else:
                self.sw3 = sw3
            if sw4 is None:
                sw4 = self.sw4
            else:
                self.sw4 = sw4

        #return correct offset depending of switch configurationFile
        if sw3 == 2:
            value = {"noise-soure":self.swtchConf["loss"]["J{0}-J18".format(sw1+8)]}
        elif sw3 == 4 and sw4 == 2:
            value = {"pwr-meter":self.swtchConf["loss"]["J{0}-J2".format(sw1+8)],
                    "fsv-fswr":self.swtchConf["loss"]["J{0}-J5".format(sw1+8)],
                    "smb100a":self.swtchConf["loss"]["J{0}-J4_20dB".format(sw1+8)]}
        elif sw3 == 4 and sw4 == 1:
            value = {"pwr-meter":self.swtchConf["loss"]["J{0}-J2".format(sw1+8)],
                    "fsv-fswr":self.swtchConf["loss"]["J{0}-J5".format(sw1+8)]}
        elif sw3 == 3 and sw4 == 2:
            value = {"smbv100a":self.swtchConf["loss"]["J{0}-J3".format(sw1+8)]}
        elif sw3 == 3 and sw4 == 1:
            value = {"smbv100a":self.swtchConf["loss"]["J{0}-J3".format(sw1+8)],
                    "smb100a":self.swtchConf["loss"]["J{0}-J4".format(sw1+8)]}
        else:
            raise commutRackException()
        
        self.log.debug("Get offset : {}".format(value))
        return value
