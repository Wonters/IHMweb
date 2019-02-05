#!/usr/bin/python2.7 
# coding=UTF-8

import argparse
import sys
import json

from pprint import pprint 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

DATABASE_IP = "127.0.0.1"
DATABASE_PORT = "27017"
DATABASE_NAME = "acbbs-configuration"
DATABASE_MAXDELAY = 500

class database(object):
    def __init__(self):
        self.__openDataBase()

    def __openDataBase(self):
        #get server, port and database from json configuration file
        server = DATABASE_IP
        port = DATABASE_PORT
        database = DATABASE_NAME
        maxSevSelDelay = DATABASE_MAXDELAY

        try:
            #open MongoDB server
            self.client = MongoClient(server, int(port), serverSelectionTimeoutMS=maxSevSelDelay)

            #check if connection is well
            self.client.server_info()
        except ServerSelectionTimeoutError as err:
            print("{0}".format(err))
            exit(0)

        #open MongoDB database
        self.db = self.client[database]

    def get_available_collection(self):
        return self.db.list_collection_names()

    def get_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
            exit(0)
        return self.db[collection].find({})

    def writeDataBase(self, document, collection):
        if collection in self.get_available_collection():
            print("Error: conf {0} exist. You can delete it with --delete {0}".format(collection))
            exit(0)

        self.db_collection = self.db[collection]
        try:
            self.db_collection.insert_one(document).inserted_id
        except DuplicateKeyError as err:
            print("{0}".format(err))

    def delete_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
            exit(0)
        self.db.drop_collection(collection)


def main(args):
    d = database()

    if args.list:
        for col in d.get_available_collection():
            print(col)

    if args.write:
        try:
            with open(args.write) as json_file:
                json_allConf = json.load(json_file)

        except IOError as err:
            print("{0}".format(err))
            exit(0)
        
        else:
            d.writeDataBase(json_allConf, args.write.split(".json")[0])

    if args.delete:
        d.delete_collection(args.delete)

    if args.read:
        for doc in d.get_collection(args.read):
            pprint(doc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Configurations assistant for ACBBS",
        fromfile_prefix_chars = '@' )
    parser.add_argument(
        "-w",
        "--write",
        help="inputfile to write in database",
        required = False)
    parser.add_argument(
        "-l",
        "--list",
        help="list all configurations stored in database",
        required = False,
        action="store_true")
    parser.add_argument(
        "-r",
        "--read",
        help="read configuration",
        required = False)
    parser.add_argument(
        "-d",
        "--delete",
        help="delete configuration",
        required = False)
    args = parser.parse_args()
    main(args)