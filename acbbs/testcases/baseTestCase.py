# coding=UTF-8

from acbbs.tools.dataBase import *
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *
from acbbs.drivers.dut import *

from threading import Thread

import time

class st():
    NOT_RUNNING = "NOT_RUNNING"
    INIT = "INIT"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ABORTING = "ABORTING"
    FINISHED = "FINISHED"

class baseTestCase(Thread):
    def __init__(self):
        #init thread
        Thread.__init__(self)

        #init var
        self.progress = 0.0
        self.status = st().NOT_RUNNING
        self.iterationsNumber = 0.0

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #init dataBase
        self.db = dataBase(file = self.__class__.__name__)

        #get configuration testcases
        self.conf = configurationFile(file = self.__class__.__name__)
        self.tcConf = self.conf.getConfiguration()

        #get date key value
        self.date = time.time()

    def getProgress(self):
        return (self.progress/self.iterationsNumber)*100.0

    def getStatus(self):
        return self.status

    def run(self):
        """


        @return  :
        @author
        """
        raise NotImplementedError()

    def abort(self):
        self.logger.debug("Aborting \"{0}\"........".format(self.__class__.__name__))
        self.status = st().ABORTING

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
