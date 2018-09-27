# coding=UTF-8

from ..tools.log import get_logger, AcbbsError

import json
from os import getcwd
from os.path import basename, splitext, realpath

class configurationFile(object):
    dutGlobal = None
    def __init__(self, file = None, simulate = False, taphw = None):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.debug("Init configurationFile in Simulate")
        else :
            self.logger.debug("Init configurationFile")
        if taphw is not None:
            configurationFile.dutGlobal = taphw

        self.file = file
        self.__openConfigurationFile()

    def getVersion(self):
        self.logger.debug("Get Version")
        return self.json_allConf["global"]["version"]

    def getConfiguration(self):
        self.logger.debug("Get configuration for \"{0}\"".format(self.file))
        try :            
            return self.json_allConf[self.file]
        except:
            raise AcbbsError("Errors: Configuration {0} not present".format(self.file))   

    def getFrequencies(self):
        self.logger.debug("Get frequencies for \"{0}\"".format(self.file))
        try:
            radioConfiguration = self.json_allConf[self.file]["radio_configuration"]
            freq_list_tx = []
            freq_list_rx = []
            for rc in radioConfiguration:
                freq_list_tx.append(self.json_allConf["global"]["radio_configuration"][rc]["freq_tx"])
                freq_list_rx.append(self.json_allConf["global"]["radio_configuration"][rc]["freq_rx"])

            #remove lists tab
            freq_tx = []
            freq_rx = []
            for freq in freq_list_tx:
                for f in freq:
                    freq_tx.append(f)
            for freq in freq_list_rx:
                for f in freq:
                    freq_rx.append(f)

            return freq_tx, freq_rx

        except:
            raise AcbbsError("Errors: Frequencies {0} not present".format(self.file))  

    def getFilters(self):
        self.logger.debug("Get filters for \"{0}\"".format(self.file))
        try:
            radioConfiguration = self.json_allConf[self.file]["radio_configuration"]
            filter_list_tx = []
            filter_list_rx = []
            for rc in radioConfiguration:
                filter_list_tx.append(self.json_allConf["global"]["radio_configuration"][rc]["filter_tx"])
                filter_list_rx.append(self.json_allConf["global"]["radio_configuration"][rc]["filter_rx"])

            #remove lists tab
            filter_tx = []
            filter_rx = []
            for filter in filter_list_tx:
                for f in filter:
                    filter_tx.append(f)
            for filter in filter_list_rx:
                for f in filter:
                    filter_rx.append(f)

            return filter_tx, filter_rx

        except:
            raise AcbbsError("Errors: Filters {0} not present".format(self.file))  


    def getBackoff(self):
        backoff = []
        bo = self.json_allConf[self.file]["backoff"]
        if isinstance(bo,(list,)):
            for backoffTc in bo:
                for backoffGlobal in self.json_allConf["global"]["backoff"]:
                    if "BO Step {0}".format(backoffTc) == backoffGlobal[0]:
                        backoff.append(backoffGlobal)
            return backoff
        else:
            for backoffGlobal in self.json_allConf["global"]["backoff"]:
                if "BO Step {0}".format(bo) == backoffGlobal[0]:
                    return backoffGlobal

    def __openConfigurationFile(self):
        with open("/etc/acbbs/configuration.json") as json_file:
            self.json_allConf = json.load(json_file)                
        if configurationFile.dutGlobal is not None:
            with open(configurationFile.dutGlobal) as json_file:
                self.json_allConf.update(json.load(json_file))
        
