# coding=UTF-8

from acbbs.tools.dataBase import *
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

class baseTestCase(object):
    def __init__(self):
        self.progress = None
        self.status = None

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #init dataBase
        self.db = dataBase(file = self.__class__.__name__)

        #get configuration testcases
        self.conf = configurationFile(file = self.__class__.__name__)
        self.tcConf = self.conf.getConfiguration()

        #get date key value
        self.date = strftime("%Y_%m_%d_%H_%M_%S")

    def getProgress(self):
        return self.progress

    def getStatus(self):
        return self.status

    def run(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def abort(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def tcInit(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def __getATEInformations(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()
