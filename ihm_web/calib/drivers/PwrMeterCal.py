import Gpib
from acbbs.tools.log import get_logger

ANRITSU_ADRESS = 4


class PowerMeterCal(object):
    class _simulate(object):
        def __init__(self):
            return

        def read(self):
            return b'0'

        def write(self):
            return b'0'

    def __init__(self, simulate=False):
        self.logger = get_logger(self.__class__.__name__)
        # self.conf = configurationFile(file = self.__class__.__name__)   a rajouter dans le fichier de configuration
        # self.pwrMeterConf = self.conf.getConfiguration()

        self.simulate = simulate
        if not self.simulate:
            self.logger.info('Init the power meter Anritsu')
            self.instrument = Gpib.Gpib(0, ANRITSU_ADRESS)  # remplacer ADRESS par l'adress du fichier de configuration

        else:
            self.logger.info('Power meter Anritsu in simulate')
            self.instrument = self._simulate()

    @property
    def info(self):
        self.logger.debug("Get info")
        if not self.simulate:
            self.instrument.write("*RST; *IDN?")
            idn = self.instrument.read(100)
        else:
            idn = "simulate"
        return idn

    @property
    def status(self):
        self.logger.debug("Get status")
        if not self.simulate:
            self.instrument.write("*RST; *STB?: *CLS")
            status = self.instrument.read(100)
        else:
            status = "simulate"
        self.logger.debug("status Anritsu:{0}".format(status))
        return status

    def power(self, nbr_mes):
        self.logger.debug("Get power")
        if not self.simulate:
            mes = "*RST; ON 1, " + str(nbr_mes)
            self.instrument.write(mes)
            listpower_b = self.instrument.read(100)
            listpower = listpower_b.decode("utf-8").split(',')
            for i in range(len(listpower)):
                listpower[i] = float(listpower[i].replace(',', '.'))
            if nbr_mes == 1:
                power = listpower[0]
            else:
                power = listpower
        else:
            power = 0.0

        return power

    @property
    def clear(self):
        self.logger.debug("Clear GPIB status bytes ")
        self.instrument.write("*CLS")
