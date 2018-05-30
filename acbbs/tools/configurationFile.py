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
        return self.json_data_global["global"]["version"]

    def getConfiguration(self):
        self.logger.debug("Get configuration for \"{0}\"".format(self.file))
        try :      
            return self.json_allConf[self.file]
        except:
            raise AcbbsError("Errors: Configuration {0} not present".format(self.file))
            


    def getBackoff(self):
        backoff = []
        bo = self.json_allConf[self.file]["backoff"]

        for backoffGlobal in self.json_data_global["global"]["backoff"]:
            if "BO Step {0}".format(bo) == backoffGlobal[0]:
                return backoffGlobal

    def __openConfigurationFile(self):
        with open("/etc/acbbs/configuration.json") as json_file:
            self.json_allConf = json.load(json_file)
        if configurationFile.dutGlobal is not None:
            with open(configurationFile.dutGlobal) as json_file:
                self.json_allConf.update(json.load(json_file))
        
