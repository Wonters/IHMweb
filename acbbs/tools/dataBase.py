# coding=UTF-8

from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from time import strftime

class dataBase(object):

    class _simulate(object):
        def __init__(self):
            return

    def __init__(self, file = None, simulate = False):
        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #case of simulate
        if simulate :
            self.logger.debug("Init dataBase in Simulate")
        else :
            self.logger.debug("Init dataBase")

        #get configuration dataBase
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dbConf = self.conf.getConfiguration()

        #collection name
        self.file = file

        #open dataBase
        self.__openDataBase()

        #create dictionnary
        self.bench_informations = {}
        self.configuration = {}
        self.measures = {}

    def writeDataBase(self, dutID, measures):
        self.__openCollection(dutID)
        try:
            post_id = self.db_collection.insert_one(measures).inserted_id
        except DuplicateKeyError as err:
            self.logger.error(err)
        else:
            self.logger.debug("successful writing at id : {0}".format(post_id))

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = self.dbConf["mongodb-ip"]
        port = self.dbConf["mongodb-port"]
        database = self.file
        maxSevSelDelay = self.dbConf["mongodb-maxSevSelDelay"]
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

    def __openCollection(self, collection):
        self.logger.debug("Create collection {0}".format(collection))

        #create collection
        self.db_collection = self.db[collection]
