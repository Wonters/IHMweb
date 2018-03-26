# coding=UTF-8

from acbbs.tools.log import *

import json
from os import getcwd
from os.path import basename, splitext

class configurationFile(object):
    def __init__(self, file = None, simulate = False):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.debug("Init configurationFile in Simulate")
        else :
            self.logger.debug("Init configurationFile")
        self.file = file
        self.__openConfigurationFile()

    def getVersion(self):
        self.logger.debug("Get Version")
        return self.json_data["global"]["version"]

    def getConfiguration(self):
        self.logger.debug("Get configuration for \"{0}\"".format(self.file))
        return self.json_data[self.file]

    def getTcIterationsNumber(self):
        nbValue = 1
        for key in self.json_data[self.file].values():
            if type(key) is list:
                nbValue *= len(key)
        return nbValue

    def __openConfigurationFile(self):
        with open("configuration.json") as json_file:
            self.json_data = json.load(json_file)
