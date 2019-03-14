import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

from .logger import logger

# Create your views here.

DATABASE_IP = "127.0.0.1"
DATABASE_PORT = "27017"
DATABASE_NAME = "acbbs-configuration"
DATABASE_MAXDELAY = 500


class database(object):

    def __init__(self):
        self.__openDataBase()

    def __openDataBase(self):
        # get server, port and database from json configuration file
        server = DATABASE_IP
        port = DATABASE_PORT
        database = DATABASE_NAME
        maxSevSelDelay = DATABASE_MAXDELAY

        try:
            # open MongoDB server
            self.client = MongoClient(server, int(port), serverSelectionTimeoutMS=maxSevSelDelay)

            # check if connection is well
            self.client.server_info()
        except ServerSelectionTimeoutError as err:
            print("{0}".format(err))
            exit(0)

        # open MongoDB database
        self.db = self.client[database]

    def get_available_collection(self):
        return self.db.list_collection_names()

    def get_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
        return self.db[collection].find({})

    def writeDataBase(self, document, collection):
        if collection in self.get_available_collection():
            print("Error: conf {0} exist. You can delete it with --delete {0}".format(collection))

        self.db_collection = self.db[collection]
        try:
            self.db_collection.insert_one(document).inserted_id
        except DuplicateKeyError as err:
            print("{0}".format(err))

    def delete_collection(self, collection):
        if collection not in self.get_available_collection():
            print("Error: conf {0} does not exist. You can list available collection with --list".format(collection))
        self.db.drop_collection(collection)


class Configuration(View):

    def __init__(self):
        # dictionnaire qui contient le fichier de configuration json
        self.configs = {}
        # database object mongo
        self.db = database()
        # list des fichiers dans la database Mongo
        self.listConf = []
        # contient le scheduler du fichier de configuration
        self.scheduler = {}

        # INITIALISATION
        self.configName = 'configuration_TAPMV4.0'
        try:
            logger.info('Configuration class initialization with the file :{0}'.format(self.configName))
            self.get_listMongo()
            self.get_conf()
            self.get_scheduler()
        except KeyError:
            logger.error("Can't INITIALIZE")
            HttpResponse("ERROR")

    # home
    def home(self, request):
        self.init(request)
        print(self.configName)
        return render(request, 'config/home.html', {'listConf': self.listConf})

    def get_listMongo(self):
        try:
            self.listConf = self.db.get_available_collection()
            self.listConf.remove('system.indexes')
            logger.info('GET list mongo')
        except ValueError as err:
            logger.error("Mongo db is not connect, open the server with cmd mongod, \n error {0}".format(err))

    def get_nameConf(self, request):
        if request.method == 'POST':
            if 'configname' in request.POST.keys():
                self.configName = str(dict(request.POST)['configname'][0])
                logger.info("GET POST: {0}".format(self.configName))
            else:
                logger.error("ERROR POST: get_nameConf 'configname' is not a key")
                HttpResponse("ERROR Configuration file is not define")
        else:
            logger.info("ERROR POST: no names selected")

    def get_conf(self):
        self.configs = {}
        if self.configName in self.listConf:
            for doc in self.db.get_collection(self.configName):
                self.configs = doc
                del self.configs['_id']
                del self.configs['scheduler']
            logger.info("GET configurations:")
        elif len(self.listConf) != 0:
            self.configName = self.listConf[0]
            logger.error("ERROR configName is not in the list, the first conf of the list be choosed")
        else:
            logger.error("list is empty")

    def get_scheduler(self):
        try:
            if self.configName in self.listConf:
                for doc in self.db.get_collection(self.configName):
                    self.configs = doc
                self.scheduler = self.configs['scheduler']
            else:
                logger.error('scheduler cant be got {0}'.format(self.scheduler))
        except KeyError as err:
            logger.error("KEy error {0}".format(err))

    def init(self, request):
        print("INITIALISATION")
        try:
            self.get_listMongo()
            self.get_nameConf(request)
            self.get_conf()
            self.get_scheduler()
        except KeyError as err:
            logger.error("key error {0}".format(err))
            HttpResponse("ERROR INITIALISATION CONFIGURATION CLASS")

    # affiche la configuration complète
    def read(self, request):
        logger.debug("before : {0} ".format(self.configs.keys()))
        self.init(request)
        del self.configs['_id']
        del self.configs['scheduler']
        if '_id' in self.configs.keys():
            return HttpResponse("Problème de suppression du dico: la clé _id est présente")
        else:
            return render(request, 'config/showconfig.html', {'configs': self.configs, 'name': self.configName})

    # crée un fichier de configuration
    def create(self, request):
        self.init(request)  # init the configuration (configs, name)
        del self.configs['_id']
        del self.configs['scheduler']
        configs_json = json.dumps(self.configs)
        return render(request, 'config/createconfig_v2.html', {'configs': self.configs, 'configs_json': configs_json,
                                                               'testcases': self.get_testcases(),
                                                               'name': self.configName})

    # écrit un fichier de configuration dans la base de donnée mongo !!!!!!! remplacer par save
    def write(self, request):
        if request.method == 'POST':
            configToWrite = dict(request.POST)
            # self.configs[]
            for key, values in configToWrite.items():
                print("la clé :", key, "/n la valeur :", values)
        else:
            logger.error("ERROR POST: saved config setup failed")
        return HttpResponse("template de redirection à définir : doit écrire "
                            "le fichier de configuration créer dans la db")

    # supprime un ifchier de la base de donnée
    def delete(self, request):
        try:
            self.db.delete_collection(self.configName)
            self.init(request)
            return render(request, 'config/home.html', {'listConf': self.listConf})

        except IOError as err:
            logger.error("ERROR delete {0}".format(err))
            return HttpResponse("ERROR deleting file")

    def add(self, request):
        nameConfAdd = dict(request.POST)["nameConfAdd"][0]
        print(nameConfAdd)
        print(type(nameConfAdd))
        try:
            with open(nameConfAdd) as json_file:
                conf = json.load(json_file)
        except IOError as err:
            print("{0}".format(err))
            return HttpResponse("File doesn't exist: maybe add the file in parent/config/")
        else:
            self.db.writeDataBase(conf, nameConfAdd.split('.json')[0])
            self.init(request)
            logger.debug("fichier {0} enregistré sur la base de donnée".format(nameConfAdd))
            return render(request, 'config/home.html', {'listConf': self.listConf})

    # retourne un dictionnaire de la forme {'mode tc': nbr de testcases dans le mode}  MAUVAISE programmation
    def get_testcases(self):
        list = []
        testcases = {}
        tc = self.scheduler["tc2play"]
        for mode in tc:
            for i in range(len(self.configs[mode])):
                list.append(i)
            testcases[mode] = list
            list = []
        return testcases

    # renvoie le testcase demander par formulaire sur un template showtc.html
    def read_testcase(self, request):
        if request.method == 'POST':
            form = request.POST['testcase']
            numConf = int(form.split(',')[0])
            nameTc = form.split(',')[1]
            logger.debug(self.configs['rxExcursion'][0]['voltage'])
            tc = self.configs[nameTc][numConf]
            logger.debug(self.configName, tc)
            return render(request, "config/showtc.html", {"testcase": tc})
        else:
            return HttpResponse("ERROR POST ")
