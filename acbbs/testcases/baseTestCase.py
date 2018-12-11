# coding=UTF-8


from ..tools.dataBase import dataBase
from ..tools.configurationFile import configurationFile
from ..tools.log import get_logger, AcbbsError
from threading import Thread

class st():
    NOT_RUNNING = "NOT_RUNNING"
    INIT = "INIT"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ABORTING = "ABORTING"
    FINISHED = "FINISHED"

class baseTestCase(Thread):
    def __init__(self, temp, simulate, conf, comment, date, channel):
        #init thread
        Thread.__init__(self)

        #init var
        self.iteration = 0
        self.status = st().NOT_RUNNING
        self.iterationsNumber = 0.0

        #store var
        self.temp = temp
        self.simulate = simulate
        self.comment = comment
        self.date = date
        self.channel = channel

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #init dataBase
        self.db = dataBase(file = self.__class__.__name__, simulate = simulate)

        #get configuration testcases
        self.conf = configurationFile(file = self.__class__.__name__)
        self.tcConf = conf

        #parse frequencies
        freq_tx, freq_rx = self.conf.getFrequencies(self.tcConf["radio_configuration"])        
        if len(self.tcConf["freq_tx"]) == 0:
            self.tcConf["freq_tx"] = freq_tx
        if len(self.tcConf["freq_rx"]) == 0:
            self.tcConf["freq_rx"] = freq_rx

        #parse filters
        filter_tx, filter_rx = self.conf.getFilters(self.tcConf["radio_configuration"])
        if len(self.tcConf["filter_tx"]) == 0:
            self.tcConf["filter_tx"] = filter_tx
        if len(self.tcConf["filter_rx"]) == 0:
            self.tcConf["filter_rx"] = filter_rx

        #check for filters and frequencies number
        if len(self.tcConf["filter_tx"]) != len(self.tcConf["freq_tx"]):
            raise AcbbsError("Errors: filter_tx and freq_tx lists has not the same size.")  
        if len(self.tcConf["filter_rx"]) != len(self.tcConf["freq_rx"]):
            raise AcbbsError("Errors: filter_rx and freq_rx lists has not the same size.")  

    @property
    def percent(self):
        return (self.iteration/self.iterationsNumber)*100.0

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
