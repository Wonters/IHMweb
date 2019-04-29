# coding=UTF-8

from ..tools.log import get_logger, AcbbsError

import json
from os import getcwd
from os.path import basename, splitext, realpath

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

class dataBaseConfiguration(object):
    def __init__(self, ip, port, name, maxDelay):
        #init logs
        self.logger = get_logger(self.__class__.__name__)

        self.databaseIP = ip
        self.databasePort = port
        self.databaseName = name
        self.max_delay = maxDelay

        self.__openDataBase()

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = self.databaseIP
        port = self.databasePort
        database = self.databaseName
        maxSevSelDelay = self.max_delay
        self.logger.debug("Open MongoDB database \"{0}\" at : {1}:{2}".format(database, server, port))

        try:
            #open MongoDB server
            self.client = MongoClient(server, int(port), serverSelectionTimeoutMS=maxSevSelDelay)

            #check if connection is well
            self.client.server_info()
        except ServerSelectionTimeoutError as err:
            self.logger.error(err)
            exit(0)

        #open MongoDB database
        self.db = self.client[database]

    def get_available_collection(self):
        return self.db.list_collection_names()

    def get_collection(self, collection):
        self.logger.debug("Open collection {0}".format(collection))
        if collection not in self.get_available_collection():
            self.logger.error("conf {0} does not exist.".format(collection))
            exit(0)
        else:
            return self.db[collection].find({})

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
        self.__openConfigurationFiles()

        self.d = dataBaseConfiguration(self.json_allConf["dataBaseConfiguration"]["ip"], self.json_allConf["dataBaseConfiguration"]["port"], self.json_allConf["dataBaseConfiguration"]["database"], self.json_allConf["dataBaseConfiguration"]["maxSevSelDelay"])
        self.__openDUTConfigurationFile()

    def getVersion(self):
        self.logger.debug("Get Version")
        return self.json_allConf["global"]["version"]

    def getConfKeys(self):
        config = {}
        for doc in self.d.get_collection(configurationFile.dutGlobal):
            config.update(doc)
        try:
            config.pop("_id")
        except:
            pass
        return list(config.keys())

    def getConfiguration(self, file=None):
        if file is None:
            file = self.file
        self.logger.debug("Get configuration for \"{0}\"".format(file))
        try :            
            return self.json_allConf[file]
        except:
            raise AcbbsError("Errors: Configuration {0} not present".format(file))   

    def getFrequencies(self, radioConfiguration):
        self.logger.debug("Get frequencies for \"{0}\"".format(self.file))
        try:
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

    def getFilters(self, radioConfiguration):
        self.logger.debug("Get filters for \"{0}\"".format(self.file))
        try:
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


    def getBackoff(self, bo):
        backoff = []
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

    def __openConfigurationFiles(self):
        with open("/etc/acbbs/configuration.json") as json_file:
            self.json_allConf = json.load(json_file)
        with open("/etc/acbbs/swtch_cal.json") as json_file:
            self.json_allConf["Swtch"].update(json.load(json_file))

    def __openDUTConfigurationFile(self):
        if configurationFile.dutGlobal is not None:
            for doc in self.d.get_collection(configurationFile.dutGlobal):
                self.json_allConf.update(doc)
        
