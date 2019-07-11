import json
import os

from acbbs.tools.log import get_logger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

from .forms import UploadFileForm

import configuration

# Create your views here.

log = get_logger('conf')

DATABASE_IP = configuration.DATABASE_IP
DATABASE_PORT = configuration.DATABASE_PORT
DATABASE_NAME = configuration.DATABASE_NAME
DATABASE_MAXDELAY = configuration.DATABASE_MAXDELAY

CONFIGFILES = configuration.CONFIGFILES


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

        # INITIALISATION
        self.nameConf = ''
        try:
            self.get_listConf()
            self.get_conf()
            log.info('init with the conf: {0}'.format(self.nameConf))
        except KeyError:
            log.error("Can't INITIALIZE")
            HttpResponse("ERROR")

    # home
    def home(self, request):
        print('HOME CONF')
        self.init(request)
        return render(request, 'config/home.html', {'listConf': self.listConf})

    def get_listConf(self):
        try:
            self.listConf = self.db.get_available_collection()
            if 'system.indexes' in self.listConf:
                self.listConf.remove('system.indexes')
            log.debug('GET list mongo')
        except ValueError as err:
            log.error("Mongo db is not connect, open the server with cmd mongod, \n error {0}".format(err))

    def get_nameConf(self, request):
        if request.is_ajax:
            try:
                self.nameConf = str(dict(request.GET)['configname'][0])
                log.debug("GET POST: {0}".format(self.nameConf))
            except KeyError as err:
                log.debug("no names selected {0}".format(err))
        elif request.method == 'POST':
            try:
                if 'configname' in request.POST.keys():
                    self.nameConf = str(dict(request.POST)['configname'][0])
                    log.debug("POST: {0}".format(self.nameConf))
                else:
                    log.error("POST: get_nameConf 'configname' is not a key")
                    HttpResponse("Configuration file is not define")
            except KeyError as err:
                log.debug("POST: no names selected {0}".format(err))
        else:
            try:
                if self.listConf != []:
                    self.nameConf = self.listConf[0]
            except ValueError as err:
                log.error("listConf is empty {0}".format(err))

    def get_conf(self):
        self.configs = {}
        if self.nameConf in self.listConf:
            for doc in self.db.get_collection(self.nameConf):
                self.configs = doc
                if '_id' in self.configs.keys():
                    del self.configs['_id']
            log.info("configuration:{0}".format(self.nameConf))
        elif len(self.listConf) != 0:
            self.nameConf = self.listConf[0]
            log.debug("init with the first conf of the list")
        else:
            log.error("collection mongo is empty")

    def init(self, request):
        log.info("init configuration")
        try:
            self.get_listConf()
            self.get_nameConf(request)
            self.get_conf()
        except KeyError as err:
            log.error("key error {0}".format(err))
            HttpResponse("ERROR INITIALISATION CONFIGURATION CLASS")

    def initWindow(self, request):
        try:
            self.init(request)
            return JsonResponse({'listConf': self.listConf, 'name': self.nameConf})
        except OSError as err:
            return HttpResponse("ERROR system {0}".format(err))

    # affiche la configuration complète
    def read(self, request):
        log.debug("read : {0} ".format(self.configs.keys()))
        if '_id' in self.configs.keys():
            del self.configs['_id']
        if 'scheduler' in self.configs.keys():
            del self.configs['scheduler']
        return render(request, 'config/showconfig.html', {'configs': self.configs, 'name': self.nameConf})

    # prend les testcases au format voulu
    def get_confType(self):
        confs_json = []
        try:
            for conf in CONFIGFILES:
                with open(conf) as conf_json:
                    confs_json.append(conf_json.read())
                    log.info("load testcase {0}".format(conf))
        except OSError as err:
            log.error(' testcase .json does not exist: {0}'.format(err))
        return json.dumps(confs_json)

    # créer un fichier de configuration
    def create(self, request):
        return render(request, 'config/createconfig_v2.html', {'type_config': self.get_confType()})

    # écrit un fichier de configuration dans la base de donnée mongo
    def save(self, request):
        if request.is_ajax():
            configToWrite = dict(request.GET)
            name = configToWrite['conf'][0]
            log.debug("save: {0}".format(configToWrite))
            log.info('configuration {0} saved'.format(name))
            file = configToWrite['data'][0]
            json_file = json.loads(file)
            if name in self.listConf:
                self.delete(request)
                log.info('configuration {0} modified'.format(name))
                print('The configuration', name, 'has been modified')
            self.db.writeDataBase(json_file, configToWrite['conf'][0])
            self.init(request)
        else:
            log.error("POST: save conf failed")
        return JsonResponse({"reponse": "valide"})

    # supprime un fichier de la base de donnée
    def delete(self, request):
        try:
            if request.is_ajax():
                confName_to_delete = dict(request.GET)['conf'][0]
                log.debug("configuration {0} delete".format(confName_to_delete))
                if confName_to_delete in self.listConf:
                    self.db.delete_collection(confName_to_delete)
                    log.info("file {0} is delete".format(confName_to_delete))
                    self.init(request)
                    return render(request, 'config/home.html', {'listConf': self.listConf})
                else:
                    return render(request, 'config/home.html', {'listConf': self.listConf})

        except IOError as err:
            log.error("delete error : {0}".format(err))
            return HttpResponse("ERROR deleting file")

    def add(self, request):
        # gerer les erreurs avec les exeptions
        if request.method == 'POST':
            fileform = UploadFileForm(request.POST, request.FILES)
            if fileform.is_valid():
                # possible to save
                file_save = json.loads(fileform.cleaned_data['file'].read().decode("utf-8"))
                file_name = fileform.cleaned_data['file'].name.split('.json')[0]
                if '_id' in file_save.keys():
                    del file_save['_id']
                if 'scheduler' in file_save.keys():
                    del file_save['scheduler']
                self.db.writeDataBase(file_save, file_name)
                self.init(request)
                log.debug("fichier {0} enregistré sur la base de donnée".format(file_name))
                return render(request, 'config/home.html', {'listConf': self.listConf})
        else:
            print("loading new file in the database failed")
            return HttpResponse("File doesn't exist: maybe add the file in parent/conf/")

    # retourne un dictionnaire de la forme {'mode tc': nbr de testcases dans le mode}  MAUVAISE programmation
    def get_testcases(self):
        list = []
        testcases = {}
        tc = self.configs.keys()
        for mode in tc:
            for i in range(len(self.configs[mode])):
                list.append(i)
            testcases[mode] = list
            list = []
        return testcases

    # NOT USE: this option is now in a toggle
    # renvoie le testcase sur un template showtc.html
    def read_testcase(self, request):
        if request.method == 'POST':
            form = request.POST['carac']
            numConf = int(form.split(',')[0])
            nameTc = form.split(',')[1]
            tc = self.configs[nameTc][numConf]
            return render(request, "config/showtc.html", {"carac": tc})
        else:
            return HttpResponse("ERROR POST read tc ")
