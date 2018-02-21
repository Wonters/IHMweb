# coding=UTF-8

from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

from os.path import basename, splitext
from pymongo import MongoClient

import time

class dataBase(object):

    class _simulate(object):
        def __init__(self):
            return

    def __init__(self, collection = None, simulate = False):
        self.logger = get_logger(splitext(basename(__file__))[0])
        if simulate :
            self.logger.debug("Init dataBase in Simulate")
        else :
            self.logger.debug("Init dataBase")

        self.conf = configurationFile(file = splitext(basename(__file__))[0])
        self.collection = "{0}_{1}".format(collection, time.strftime("%Y_%m_%d_%H_%M_%S"))

        self.__openDataBase()
        self.__createCollection()

    def writeDataBase(self, **kwargs):
        for key in kwargs:
            self.logger.debug("Write in database : {0} \"{1}\":\"{2}\"".format(self.collection, key, kwargs[key]))
            post = {key:kwargs[key]}
            post_id = self.db_collection.insert_one(post).inserted_id
            self.logger.debug("successful writing at id : {0}".format(post_id))

    def readDataBase(self, id = None, param = None):
        """


        @param string id :
        @param string param :
        @return  :
        @author
        """
        pass

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = self.conf.getConfiguration("mongodb-ip")
        port = self.conf.getConfiguration("mongodb-port")
        database = self.conf.getConfiguration("mongodb-database")
        self.logger.debug("Open MongoDB database \"{0}\" at : {1}:{2}".format(database, server, port))

        #open MongoDB server
        self.client = MongoClient(server, int(port))

        #open MongoDB database
        self.db = self.client[database]

    def __createCollection(self):
        self.logger.debug("Create collection {0}".format(self.collection))

        #create collection
        self.db_collection = self.db[self.collection]
