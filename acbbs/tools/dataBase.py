# coding=UTF-8
from acbbs.tools.log import *

from os.path import basename, splitext

class dataBase(object):

    class _simulate(object):
        def __init__(self):
            return

    def __init__(self, name = None, simulate = False):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.info("Init dataBase in Simulate")
            self._dev = self._simulate()
        else :
            self.logger.info("Init dataBase")
            self.database = self.__openDataBase()

    def writeDataBase(self, **kwargs):
        """


        @param  _kwargs :
        @return  :
        @author
        """
        pass

    def readDataBase(self, id = None, param = None):
        """


        @param string id :
        @param string param :
        @return  :
        @author
        """
        pass

    def __openDataBase(self):
        """


        @return  :
        @author
        """
        pass
