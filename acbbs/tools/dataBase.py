# coding=UTF-8

from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from os.path import basename, splitext
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

import time

class dataBase(object):

    class _simulate(object):
        def __init__(self):
            return

    def __init__(self, collection = None, simulate = False):
        #init logs
        self.logger = get_logger(splitext(basename(__file__))[0])

        #case of simulate
        if simulate :
            self.logger.debug("Init dataBase in Simulate")
        else :
            self.logger.debug("Init dataBase")

        #get configuration dataBase
        self.conf = configurationFile(file = splitext(basename(__file__))[0])
        self.dbConf = self.conf.getConfiguration()

        #collection name
        self.collection = "{0}_{1}".format(collection, time.strftime("%Y_%m_%d_%H_%M_%S"))

        #open dataBase
        self.__openDataBase()
        self.__createCollection()

        #create dictionnary
        self.bench_informations = {}
        self.configuration = {}
        self.measures = {}

    def writeDataBase(self, measures):
        post_id = self.db_collection.insert_one(measures).inserted_id
        self.logger.debug("successful writing at id : {0}".format(post_id))

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = self.dbConf["mongodb-ip"]
        port = self.dbConf["mongodb-port"]
        database = self.dbConf["mongodb-database"]
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

    def __createCollection(self):
        self.logger.debug("Create collection {0}".format(self.collection))

        #create collection
        self.db_collection = self.db[self.collection]
