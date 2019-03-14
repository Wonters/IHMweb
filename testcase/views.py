#!/usr/bin/python3 
# coding=UTF-8

import json

from acbbs import __version__
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from config.views import Configuration
from .forms import testcaseForm
from .logger import logger
from .models import *
from .tasks import *

CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8]

TESTCASES = {
    "rxExcursion": rxExcursion,
    "txExcursion": txExcursion,
    "txIM3Measurement": txIM3Measurement
}


class Caracterisation(View):

    def __init__(self):
        # configuration de la commande acbbs-scheduler
        self.cmd = {}
        # list des thread à lancer scheduler__start PAS UTILE DE LE GARDER DANS CET OBJECT
        self.threadTc_list = []
        # liste des entrées du switch auxquelles sont connectés les stations de base
        self.channels = CHANNELS
        # booléen qui commande l'arrết du start_scheduler
        self.stopschedule = bool
        # class qui se charge de la manipulation des fichiers json et de la db mongo
        self.cf = Configuration()
        # variable qui renvoie l'avancement au front end par requète ajax
        self.progress = {'current': 0, 'total': 0, 'tc_current': 0, 'tc_total': 0, 'tc': '',
                         'temperature': 0}
        # scheduler de commande {rxExcursion : [1,2,3], txExcursion : [1,2], txMMeasurement: [0]}
        # envoyé par le front-end
        self.schedule = {'temperature': [], 'tc2play': {},
                         'delay': 0}

    # Home renvoie le template home de l'application testcase
    def home(self, request):
        if len(self.cf.listConf) == 0:
            print("MONGO SERVER is not opened")
            return HttpResponse('MONGO SERVER IS NOT OPENED check mongo with followed shell cmd: /n ps -wuax | mongo '
                                '/n if mongo is running, sudo killall mongo and sudo mongod ')
        else:
            self.cf.init(request)
            print("HOME")
            return self.show_scheduler(request)

    # schow_scheduler envoie le scheduler json au frontend par variable html
    def show_scheduler(self, request):
        if len(self.cf.listConf) != 0:
            logger.debug("{0}".format(self.cf.scheduler))
            temperature = self.cf.scheduler["temperature"]
            clim_chamber_delay = self.cf.scheduler["climChamberDelay"]
            listTc = self.cf.get_testcases()
        else:
            logger.warning("Mongo server is not open")
        return render(request, 'testcase/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels,
                                                         'temperature': temperature, "listTc": listTc,
                                                         "clim_chamber_delay": clim_chamber_delay})

    # load charge le fichier de configuration selectioné (formulaire envoyé par le frontend )
    def load(self, request):
        if request.method == 'POST':
            self.cf.init(request)  # initialise la class Configuration
            return self.show_scheduler(request)
        else:
            logger.error("can't load the configuration file selected")
            return render(request, 'testcase/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels})

    # affiche le tc cliqué sur le frontend (formulaire) avec le template showtc.html
    @csrf_exempt
    def readtc(self, request):
        if request.method == 'POST':
            form = request.POST['testcase']
            numConf = int(form.split(',')[0])
            nameTc = form.split(',')[1]
            tc = self.cf.configs[nameTc][numConf]
            return render(request, "config/showtc.html", {"testcase": tc})
        else:
            return HttpResponse("ERROR POST ")

    # Recupère le formulaire scheduler
    def get_parametersCmd(self, request):
        if request.method == 'POST':
            form = testcaseForm(request.POST)
            if form.is_valid():
                form.save()
                logger.debug("DEBUG: name of the carac : {0}".format(form.cleaned_data['testcase_nameCarac']))
                logger.info("formulare input: {0} ".format(form.cleaned_data))
                for i in Testcasemodel.objects.all():
                    if str(i) == form.cleaned_data['testcase_nameCarac']:
                        Testcasemodel.objects.filter(testcase_nameCarac=str(i)).delete()
                        form.save()
            else:
                logger.debug('debug: formulare is not valide')
        else:
            logger.debug("ERROR POST:", request)
        conf = dict(request.POST)
        conf["testcase_configFile"] = self.cf.configName
        conf["testcase_nameCarac"] = str(conf["testcase_type"] + list(str(time.time())) + conf["testcase_nameCarac"])
        self.cmd = dict(request.POST)
        return form.is_valid()

    # Recupère le scheduler saisit en frontend
    def write_schedule(self, request):
        if request.is_ajax():
            scheduler = dict(request.GET)
            logger.info("AJAX send:{0}".format(scheduler))
            self.schedule['tc2play'] = self.makeScheduleTc(json.loads(scheduler['tc2play'][0]))
            self.schedule['temperature'] = json.loads((scheduler['temperature'][0]))
            self.schedule['delay'] = int(scheduler['delay'][0])
            logger.info("Scheduler cmd : {0}".format(self.schedule))
        else:
            logger.warning("problème de requète ajax : write_scheduler")
        return JsonResponse({"scheduler": "ok"})

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

    # renvoie progress au frontend toute les 500ms voir js Ajax setBackend home_v2.js
    def counter(self, request):
        return JsonResponse(self.progress)

    # Lance la tâche start_scheduler
    def start(self, request):
        if (self.get_parametersCmd(request)):
            self.schedule_start
        else:
            logger.info("Scheduler starting is not valide")
            return HttpResponse("FORM is NOT VALID")
        return self.show_scheduler(request)  # retourner un json

    # Interrompt la tâche
    def stop(self, request):
        self.stopschedule = 1
        return render(request, 'testcase/home_v2.html', {'listConf': self.cf.listConf, 'channels': self.channels})

    # tâche qui lance la caractérisation
    @property
    def schedule_start(self):
        self.stopschedule = 0
        # tampon qui stocke les itération successive entre chaque tc
        step = 0
        logger.info("Start is running ....")
        if self.cmd:
            cmd = self.cmd
            cmd['testcase_configFile'] = self.cf.configName
            print("ACBBS V{} -- {}".format(__version__, time.strftime(
                "%Y-%m-%d %H:%M:%S")))
            if cmd["testcase_simulation"][0]:
                simulate = True
            else:
                simulate = False
            try:
                dut_channel = str(cmd["testcase_channel"][0]).split(
                    ",")
                for i in range(0, len(dut_channel)):
                    dut_channel[i] = int(dut_channel[i])
            except:
                print("Error parsing DUT channel")
                exit(0)
            if cmd["testcase_climChamber"][0] is False:
                clim = ClimCham(simulate=simulate)
                clim.status = 1

            # Loop
            for temp in self.schedule['temperature']:
                self.progress['temperature'] = temp
                print("\n#########################")
                print("Launch TestCases at {0} C".format(temp))
                print("#########################\n")
                if cmd["testcase_climChamber"][0] is False:
                    clim.tempConsigne = temp
                    print("Waiting for {0} seconds".format(self.schedule['delay']))
                    if not self.stopschedule:
                        for remaining in range(self.schedule['delay'], 0, -1):
                            sys.stdout.write("\r")
                            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                            sys.stdout.flush()
                            time.sleep(1)
                    else:
                        print("\n\nKeyboard Interrupt. Stop countdown....")
                        clim.status = 0
                        sys.exit(0)
                    print("\n")

                self.threadTc_list = []
                for mode, tc in self.schedule['tc2play'].items():
                    for i in tc:
                        self.threadTc_list.append(TESTCASES[mode](temp=temp, simulate=simulate,
                                                                  conf=self.cf.configs[mode][int(i)],
                                                                  comment=cmd["testcase_nameCarac"][0],
                                                                  date=time.time(),
                                                                  channel=dut_channel))
                tmp_class = ""

                # init progress backend
                if self.progress['total'] == 0:
                    for threadTc in self.threadTc_list:
                        self.progress['total'] = self.progress['total'] + threadTc.iterationsNumber
                    self.progress['total'] = self.progress['total'] * len(self.schedule['temperature'])
                    print(self.progress['total'])

                # Lance les thread pour chaque température
                for threadTc in self.threadTc_list:
                    if tmp_class != threadTc.__class__.__name__:
                        conf_number = 0
                        tmp_class = threadTc.__class__.__name__
                    conf_number += 1
                    print("Processing {0} -- Conf {1}/{2}".format(threadTc.__class__.__name__, conf_number,
                                                                  len(self.schedule['tc2play'][
                                                                          threadTc.__class__.__name__])))
                    print(time.strftime("%Y-%m-%d %H:%M:%S"))
                    bar = ProgressBar(threadTc.iterationsNumber, max_width=70)

                    # base de donnée
                    Progressbar.progress_value = threadTc.iterationsNumber

                    ## start threading
                    threadTc.tcInit()
                    threadTc.start()
                    i = threadTc.iteration

                    self.progress['tc_total'] = threadTc.iterationsNumber
                    list1 = list(threadTc.__class__.__name__) + list("-") + list(str(conf_number - 1))
                    self.progress['tc'] = ''.join(list1)

                    while threadTc.is_alive():
                        if not self.stopschedule:
                            time.sleep(0.1)
                            if threadTc.iteration != i:
                                i = threadTc.iteration
                                bar.numerator = i
                                self.progress['current'] = step + i
                                self.progress['tc_current'] = i
                                print(bar, end='\r')
                                sys.stdout.flush()
                        else:
                            print("\n\nKeyboard Interrupt Aborting ..... : threadTc was alive {0}".format(
                                threadTc.__class__.__name__))
                            threadTc.abort()
                            threadTc.join()
                            if cmd["testcase_climChamber"][0] is False:
                                clim.status = 0

                    # progression backend
                    step = step + i
            print("TestCases finished")
            if cmd["testcase_climChamber"][0] is False:
                print("Switch off climatic chamber")
                clim.status = 0
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("INPUT ERROR : all inputs are not filled ")

            # PROGRESS TO 0 #
        self.progress['current'] = 0
        self.progress['total'] = 0
        self.progress['tc_current'] = 0
        self.progress['tc_total'] = 0
        self.progress['temperature'] = 0

        return 'work is complete'
