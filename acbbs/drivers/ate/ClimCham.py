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
        return {
            # "error":self.errors,
            # "temp_consigne":self.tempConsigne,
            # "temp_real":self.tempReal,
            # "status":self.status
        }

    @property
    def errors(self):
        if not self.simulate:
            return []

        else:
            return []

    @property
    def status(self):
        return self._dev.read_holding_registers(5953, 1)[0]

    @status.setter
    def status(self, value):
        self.logger.info("Change status to %s" % value)
        self._dev.write_single_register(5953, int(value))

    @property
    def tempConsigne(self):
        return float(ctypes.c_short(self._dev.read_holding_registers(2)[0]).value) / 10
    
    @tempConsigne.setter
    def tempConsigne(self,value):
        if value > 100 or value < -50:
            raise AcbbsError("the temperature must be between -50 and 100 val : %s" % value, log = self.logger)
        self.logger.info("set temperature to %s" % value)
        self._dev.write_single_register(2, ctypes.c_ushort(int(value*10)).value)

    @property
    def tempReal(self):
        return float(ctypes.c_short(self._dev.read_holding_registers(1)[0]).value) / 10

    @property
    def humidityConsigne(self):
        return None

    @property
    def humidityReal(self):
        return None
