# coding=UTF-8

from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from os.path import basename, splitext

class dataBase(object):

    class _simulate(object):
        def __init__(self):
            return

    def __init__(self, name = None, simulate = False):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.debug("Init dataBase in Simulate")
        else :
            self.logger.debug("Init dataBase")

        self.conf = configurationFile(file = splitext(basename(__file__))[0])
        self.__openDataBase()

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
        server = self.conf.getConfiguration("mongodb-ip")
        port = self.conf.getConfiguration("mongodb-port")
        self.logger.debug("Open MongoDB at : {0}:{1}".format(server, port))
