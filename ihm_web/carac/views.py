#!/usr/bin/python3 
# coding=UTF-8

import json

from acbbs.tools.log import get_logger
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from conf.views import Configuration
from .tasks import TaskScheduler

import configuration

log = get_logger("carac")

CHANNELS = configuration.CHANNELS

class Caracterisation(View):

    def __init__(self, **kwargs):
        log.warning('carac init')
        # configuration de la commande acbbs-scheduler
        super().__init__(**kwargs)
        self.cmd = {}
        # list des thread à lancer scheduler__start PAS UTILE DE LE GARDER DANS CET OBJECT

        self.channels = CHANNELS

        # class qui se charge de la manipulation des fichiers json et de la db mongo
        self.cf = Configuration()

        # scheduler de commande {rxExcursion : [1,2,3], txExcursion : [1,2], txMMeasurement: [0]}
        # envoyé par le front-end
        self.scheduler = {'temperature': [], 'tc2play': {},
                          'climChamberDelay': 0}

        self.taskScheduler = TaskScheduler(conf=self.cf, command=self.cmd, scheduler=self.scheduler)

    # Home renvoie le template home de l'application carac
    def home(self, request):
        self.cf.init(request)
        # self.initProgress()
        print("HOME CARAC")
        return render(request, 'carac/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels,
                                                      'temperature': [], "listTc": [],
                                                      "clim_chamber_delay": 0})

    # schow_scheduler envoie le scheduler json au frontend par variable html
    def show_scheduler(self, request):
        try:
            if len(self.cf.listConf) != 0:
                log.debug("Send available testcases ")
                temperature = self.scheduler["temperature"]
                clim_chamber_delay = self.scheduler["climChamberDelay"]
                listTc = self.cf.get_testcases()
                return render(request, 'carac/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels,
                                                              'temperature': temperature, 'listTc': listTc,
                                                              'clim_chamber_delay': clim_chamber_delay})
        except KeyError as err:
            log.error("Err scheduler {0}".format(err))
            return render(request, 'carac/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels,
                                                          'temperature': [], "listTc": [],
                                                          'clim_chamber_delay': 0})

    # load charge le fichier de configuration selectioné (formulaire envoyé par le frontend )
    @csrf_exempt
    def load(self, request):
        if request.is_ajax():
            self.cf.init(request)  # initialise la class Configuration
            listTc = self.cf.get_testcases()
            log.debug('Tc2play done from : {0}'.format(self.cf.nameConf))
            return JsonResponse({'listTc': listTc})
        else:
            log.error("can't load the configuration file selected")

    # affiche le tc cliqué sur le frontend (formulaire) avec le template showtc.html
    @csrf_exempt
    def readtc(self, request):

        if request.is_ajax():
            testcase = request.GET['tc']
            numConf = int(testcase.split(',')[0])
            nameTc = testcase.split(',')[1]
            try:
                if len(self.cf.configs[nameTc]) != 0:
                    tc = self.cf.configs[nameTc][numConf]
                    return JsonResponse({"testcase": tc})
                return JsonResponse({"testcase": {}})
            except KeyError as err:
                return JsonResponse({"testcase": {}})


    # Recupère le formulaire setting
    def get_parametersCmd(self, request):
        if request.is_ajax():
            form = dict(request.GET)
            log.info('GET commands')
            log.debug('commands: {0} '.format(form))
            form["nameCarac"] = str(form["type"][0] +'_'+ form["nameCarac"][0])
            self.cmd = form
            return True
        else:
            log.debug("Err POST commands".format(request))
            return HttpResponse('ERROR POST')

    # Recupère le scheduler saisit en frontend
    def write_schedule(self, request):
        if request.is_ajax():
            scheduler = dict(request.GET)
            self.scheduler['tc2play'] = self.makeScheduleTc(json.loads(scheduler['tc2play'][0]))
            self.scheduler['temperature'] = json.loads((scheduler['temperature'][0]))
            self.scheduler['climChamberDelay'] = int(scheduler['delay'][0])
            log.debug("GET from AJAX Tc2play")
        else:
            log.warning("problème de requète ajax : write_scheduler")
        return JsonResponse({"scheduler": "ok"})

    # Lance la tâche start_scheduler
    def start(self, request):
        if self.get_parametersCmd(request) == True:
            # lancement de la tâche dans tasks
            self.taskScheduler = TaskScheduler(conf=self.cf, command=self.cmd, scheduler=self.scheduler)
            response = self.taskScheduler.start()
            return JsonResponse({'response': response})
        else:
            log.info("Scheduler is not valide")
            return HttpResponse("FORM is NOT VALID")

    # Interrompt la tâche
    def stop(self, request):
        self.taskScheduler.stopschedule = 1
        self.taskScheduler.initializeProgress()
        return JsonResponse({'response': 'stop'})

    # format le scheduler sous la forme {mode : [number du tc,],}
    def makeScheduleTc(self, tc2play):
        tc2play_format = {}
        for key, value in tc2play.items():
            tc_mode = key.split(',')[1]
            tc2play_format[tc_mode] = []
            for key2, value2 in tc2play.items():
                i = key2.split(',')[1]
                if i == tc_mode and value2:
                    tc_number = key2.split(',')[0]
                    tc2play_format[tc_mode].append(tc_number)
        return tc2play_format
