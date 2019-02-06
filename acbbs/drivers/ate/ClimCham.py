# coding=UTF-8
from ...tools.log import get_logger, AcbbsError
from ...tools.configurationFile import configurationFile

from pyModbusTCP.client import ModbusClient
import ctypes

TIMEOUT = 5

class ClimCham(object):
    class _simulate(object):
        def __init__(self):
            return
        def read_holding_registers(self, add, reg_nb=1):
            return [0]
        def write_single_register(self, add, val):
            return
            
    def __init__(self, simulate = False):

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dcConf = self.conf.getConfiguration()

        #simulation state
        self.simulate = simulate

        if not simulate:
            self.logger.info("New climatic chamber instance at {0}".format(self.dcConf["ip"]))
            self._dev = ModbusClient(host=self.dcConf["ip"], auto_open=True, auto_close=True, timeout = TIMEOUT, unit_id=255)
            
        else:
            self.logger.info("New climatic chamber instance in simulate")
            self._dev = self._simulate()

        self.reference_var = None
        self.version_var = None

    @property
    def info(self):
        self.logger.debug("Get info")
        return {
            # "error":self.errors,
            # "Oven_Prog_Temperature_(C)":self.tempConsigne,
            # "Oven_Temperature_(C)":self.tempReal,
            # "status":self.status
        }

    @property
    def errors(self):
        if not self.simulate:
            value = []
        else:
            value = []
        self.logger.debug("Get errors : {}".format(value))
        return value

    @property
    def status(self):
        value = self._dev.read_holding_registers(5953, 1)[0]
        self.logger.debug("Get status : {}".format(value))
        return value

    @status.setter
    def status(self, value):
        self.logger.debug("Set status : {}".format(value))
        self._dev.write_single_register(5953, int(value))

    @property
    def tempConsigne(self):
        value = float(ctypes.c_short(self._dev.read_holding_registers(2)[0]).value) / 10
        self.logger.debug("Get tempConsigne : {}".format(value))
    
    @tempConsigne.setter
    def tempConsigne(self,value):
        self.logger.debug("Set tempConsigne : {}".format(value))
        if value > 100 or value < -50:
            raise AcbbsError("the temperature must be between -50 and 100 val : %s" % value, log = self.logger)
        self._dev.write_single_register(2, ctypes.c_ushort(int(value*10)).value)

    @property
    def tempReal(self):
        value = float(ctypes.c_short(self._dev.read_holding_registers(1)[0]).value) / 10
        self.logger.debug("Get tempReal : {}".format(value))

    @property
    def humidityConsigne(self):
        return None

    @property
    def humidityReal(self):
        return None
