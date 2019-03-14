from __future__ import absolute_import, unicode_literals

import sys
import time

from acbbs import __version__
from acbbs.drivers.ate.ClimCham import ClimCham
from acbbs.testcases.rxExcursion import rxExcursion
from acbbs.testcases.txExcursion import txExcursion
from acbbs.testcases.txIM3Measurement import txIM3Measurement
from acbbs.tools.configurationFile import configurationFile
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from etaprogress.progress import ProgressBar

from .celery import appTestcase

TESTCASES = {
    "rxExcursion": rxExcursion,
    "txExcursion": txExcursion,
    "txIM3Measurement": txIM3Measurement
}


@appTestcase.task
def test1(seconds):
    for i in range(seconds):
        print("test1 is running", i)
        time.sleep(1)
    return 'test1 is done'


@shared_task(name="addtonumber")
def add(x, y):
    for i in range(seconds):
        print("add is running", i)
        time.sleep(1)
    return 'add is done'


# MAUVAISE IMPLÉMENTATION, PRESENCE DE SELF DANS L'INTITULÉ DE LA FONCTION ALORS QU'IL N'Y PAS DE CLASS
@shared_task(bind=True)
def test(self, seconds):
    print("task is running !!!")
    progress_recorder = ProgressRecorder(self)
    for i in range(seconds):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, seconds)
    return 'test is done'


@shared_task(name="schedule_start")
def schedule_start(stop, cmd):
    # get configuration
    stop = 0
    if cmd:
        configs = cmd
        print("les confifurations de la class carac : ", configs)
        # print date and version
        print("ACBBS V{} -- {}".format(__version__, time.strftime(
            "%Y-%m-%d %H:%M:%S")))  # convertion d'une queryset en dictionnaire

        ### A CHANGER POUR ENLEVER LE SCHEDULER DU FICHIER DE CONFIGURAITON JSON
        conf = configurationFile(file="scheduler",
                                 taphw=configs["testcase_configFile"][0])  # args.dut fichier de configuration
        schConf = conf.getConfiguration()
        if configs["testcase_simulation"][0]:
            simulate = True
        else:
            simulate = False
        try:
            dut_channel = str(configs["testcase_channel"][0]).split(
                ",")
            for i in range(0, len(dut_channel)):
                dut_channel[i] = int(dut_channel[i])
        except:
            print("Error parsing DUT channel")
            exit(0)
        # initialize climatic chamber
        if configs["testcase_climChamber"][0] is False:
            clim = ClimCham(simulate=simulate)
            clim.status = 1
        # start loops
        for temp in schConf["temperature"]:
            # set temperature and wait
            print("\n#########################")
            print("Launch TestCases at {0}C".format(temp))
            print("#########################\n")
            if configs["testcase_climChamber"][0] is False:
                print("Set climatic chamber at {0} C".format(temp))
                clim.tempConsigne = temp
                print("Waiting for {0} seconds".format(schConf["climChamberDelay"]))
                # try:
                if not stop:
                    for remaining in range(schConf["climChamberDelay"], 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                        sys.stdout.flush()
                        time.sleep(1)
                else:
                    print("\n\nKeyboard Interrupt. Stop countdown....")
                    clim.status = 0
                    sys.exit(0)
                print("\n")
            threadTc_list = []
            for tc in schConf["tc2play"]:
                for conf_number in range(0, len(conf.getConfiguration(file=tc))):
                    threadTc_list.append(TESTCASES[tc](temp=temp, simulate=simulate,
                                                       conf=conf.getConfiguration(file=tc)[conf_number],
                                                       comment=configs["testcase_nameCarac"][0],
                                                       date=time.time(),
                                                       channel=dut_channel))
            tmp_class = ""
            for threadTc in threadTc_list:
                if tmp_class != threadTc.__class__.__name__:
                    conf_number = 0
                    tmp_class = threadTc.__class__.__name__
                conf_number += 1
                print("Processing {0} -- Conf {1}/{2}".format(threadTc.__class__.__name__, conf_number, len(
                    conf.getConfiguration(file=threadTc.__class__.__name__))))
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                bar = ProgressBar(threadTc.iterationsNumber, max_width=70)

                ## start threading
                threadTc.tcInit()
                threadTc.start()
                i = threadTc.iteration
                # try:
                while threadTc.is_alive():
                    if not stop:
                        time.sleep(0.1)
                        if threadTc.iteration != i:
                            i = threadTc.iteration
                            bar.numerator = i
                            print(bar, end='\r')
                            sys.stdout.flush()
                    else:
                        print("\n\nKeyboard Interrupt Aborting ..... : threadTc was alive {0}".format(
                            threadTc.__class__.__name__))
                        threadTc.abort()
                        threadTc.join()
                        if configs["testcase_climChamber"][0] is False:
                            clim.status = 0
                        sys.exit(0)
        print("TestCases finished")
        if configs["testcase_climChamber"][0] is False:
            print("Switch off climatic chamber")
            clim.status = 0
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print("INPUT ERROR : all inputs are not filled ")  # ERROR window message
    return 'work is complete'


@shared_task(name="schedule_stop")
def schedule_stop(self, request):
    stop = int(dict(request.POST)['stop'][0])
    print("requete stop: ", dict(request.POST)['stop'])
    return 'work is complete'
