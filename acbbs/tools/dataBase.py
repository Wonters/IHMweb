# coding=UTF-8

from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

class dataBase(object):
    def __init__(self, file = None, simulate = False):
        #init logs
        self.log = get_logger(self.__class__.__name__)

        #get configuration dataBase
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dbConf = self.conf.getConfiguration()

        #case of simulate
        if simulate :
            self.log.info("Init dataBase in Simulate")
            self.simulate = True
        else :
            self.log.info("Init dataBase")
            self.simulate = False

            #open dataBase
            self.__openDataBase()

        #collection name
        self.file = file

        #create dictionnary
        self.bench_informations = {}
        self.configuration = {}
        self.measures = {}

    def writeDataBase(self, document):
        if self.simulate == True:
            self.log.debug("writing simulation")
        else:
            self.__openCollection(self.file)
            try:
                post_id = self.db_collection.insert_one(document).inserted_id
            except DuplicateKeyError as err:
                self.log.error(err)
            else:
                self.log.debug("successful writing at id : {0}".format(post_id))

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = self.dbConf["ip"]
        port = self.dbConf["port"]
        database = self.dbConf["database"]
        maxSevSelDelay = self.dbConf["maxSevSelDelay"]
        self.log.debug("Open MongoDB database \"{0}\" at : {1}:{2}".format(database, server, port))

        try:
            #open MongoDB server
            self.client = MongoClient(server, int(port), serverSelectionTimeoutMS=maxSevSelDelay)

            #check if connection is well
            self.client.server_info()
        except ServerSelectionTimeoutError as err:
            self.log.error(err)
            exit(0)

        #open MongoDB database
        self.db = self.client[database]

    def __openCollection(self, collection):
        self.log.debug("Open collection {0}".format(collection))

        #create collection
        self.db_collection = self.db[collection]
