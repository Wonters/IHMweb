# coding=UTF-8

from acbbs.tools.log import *

import json
from os import getcwd
from os.path import basename, splitext, realpath

class configurationFile(object):
    dut = None
    def __init__(self, file = None, simulate = False, taphw = None):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.debug("Init configurationFile in Simulate")
        else :
            self.logger.debug("Init configurationFile")

        if configurationFile.dut is None and taphw is None:
            raise AcbbsError("Errors: no DUT Hw defined")
        elif configurationFile.dut is not None and taphw is not None:
            raise AcbbsError("Errors: DUT Hw already defined")
        elif configurationFile.dut is None and taphw is not None:
            configurationFile.dut = taphw

        self.file = file
        self.__openConfigurationFile()

    def getVersion(self):
        self.logger.debug("Get Version")
        return self.json_data_global["global"]["version"]

    def getConfiguration(self):
        self.logger.debug("Get configuration for \"{0}\"".format(self.file))
        if self.file.startswith("rx") or self.file.startswith("tx"):
            return self.json_data_tc[self.file]
        else:
            return self.json_data_global[self.file]

    def getBackoff(self):
        backoff = []
        bo = self.json_data_tc[self.file]["backoff"]
        if isinstance(bo,(list,)):
            for backoffTc in bo:
                for backoffGlobal in self.json_data_global["global"]["backoff"]:
                    if "BO Step {0}".format(backoffTc) == backoffGlobal[0]:
                        backoff.append(backoffGlobal)
            return backoff
        else:
            for backoffGlobal in self.json_data_global["global"]["backoff"]:
                if "BO Step {0}".format(bo) == backoffGlobal[0]:
                    return backoffGlobal

    def __openConfigurationFile(self):
        path = realpath(__file__).split(self.__class__.__name__)[0]
        with open("{0}/../../configuration_{1}.json".format(path, configurationFile.dut)) as json_file:
            self.json_data_tc = json.load(json_file)
        with open("{0}/../../configuration.json".format(path)) as json_file:
            self.json_data_global = json.load(json_file)
