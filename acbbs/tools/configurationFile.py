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
        with open("acbbs/configuration.json") as json_file:
            self.json_data = json.load(json_file)

    def openConfigurationFile(self):
        """


        @return  :
        @author
        """
        pass

    def getConfiguration(self, key = None):
        self.logger.debug("Get configuration at \"{0}\"/\"{1}\":\"{2}\"".format(self.file, key, self.json_data[self.file][key]))
        return self.json_data[self.file][key]
