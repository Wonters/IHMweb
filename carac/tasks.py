from __future__ import absolute_import, unicode_literals

import time

from acbbs.drivers.ate.ClimCham import ClimCham
from acbbs.testcases.rxExcursion import rxExcursion
from acbbs.testcases.txExcursion import txExcursion
from acbbs.testcases.txIM3Measurement import txIM3Measurement
from acbbs.testcases.txPowVsFreq import txPowVsFreq
from acbbs.testcases.txOLFrequency import txOLFrequency
###########
from acbbs.tools.log import get_logger
from etaprogress.progress import ProgressBar

from .models import *

## ajouter la lib du nouveau testcase ici ##


logger = get_logger("task")

## ajouter la lib à l'intèrieure du tableau ##
TESTCASES = {
    "rxExcursion": rxExcursion,
    "txExcursion": txExcursion,
    "txIM3Measurement": txIM3Measurement,
    ##"txPowVsFreq": txPowVsFreq,
    ##"txOLFrequency": txOLFrequency,
    ## nouveau testcase ##

}


class TaskScheduler:

    def __init__(self, conf, command, scheduler):
        self.stopschedule = bool
        self.progress = {'current': 0, 'total': 0, 'tc_current': 0, 'tc_total': 0, 'tc': '',
                         'temperature': 0, 'state': 0, 'responseTask': ''}
        self.cmd = command
        self.cf = conf
        self.threadTc_list = []
        self.scheduler = scheduler

    def initializeProgress(self):
        logger.info('init progress')
        self.progress['current'] = 0
        self.progress['total'] = 0
        self.progress['tc_current'] = 0
        self.progress['tc_total'] = 0
        self.progress['temperature'] = 0
        self.progress['state'] = 0
        self.progress['responseTask'] = 'ready'
        self.progress['tc'] = ''

    def get_cmd(self):
        logger.debug("{0}".format(self.cmd))
        if self.cmd:
            self.cmd['configFile'] = self.cf.nameConf

            if self.cmd["simulate"][0] == "yes":
                logger.info("simulate")
                self.simulate = True
            else:
                self.simulate = False
                logger.info("no simulate")
            try:
                self.dut_channel = self.cmd["channel"][0].split(",")
                for i in range(0, len(self.dut_channel)):
                    self.dut_channel[i] = int(self.dut_channel[i])
            except:
                print("Error parsing DUT channel")
                breakpoint()
            if self.cmd["climChamber"][0] == "yes":
                self.clim = ClimCham(simulate=self.simulate)
                self.clim.status = 1
            logger.debug('simulate:{0}, climChamber:{1},channels: {2}'.format(self.simulate, self.cmd["climChamber"][0],
                                                                              self.dut_channel))
            return True
        else:
            logger.debug('commands are not valide')
            return False

    def get_totalProgress(self):
        if self.progress['total'] == 0:
            self.threadTc_list = []
            for mode, tc in self.scheduler['tc2play'].items():
                for tc_num in tc:
                    self.threadTc_list.append(TESTCASES[mode](temp=0, simulate=True,
                                                              conf=self.cf.configs[mode][int(tc_num)],
                                                              comment=self.cmd["nameCarac"][0],
                                                              date=time.time(),
                                                              channel=self.dut_channel))
            for threadTc in self.threadTc_list:
                self.progress['total'] = self.progress['total'] + threadTc.iterationsNumber
            self.progress['total'] = self.progress['total'] * len(self.scheduler['temperature'])

    # lance la caractérisation, dépend de la class caracatérisation
    def start(self):
        self.stopschedule = 0
        # tampon qui stocke les itération successive entre chaque tc
        step = 0
        if self.get_cmd() is True:
            # init progress backend
            self.get_totalProgress()

            logger.info("carac start ....")
            self.progress['responseTask'] = 'running'
            self.progress['state'] = 1
            ######### LOOP ###################
            for temp in self.scheduler['temperature']:
                self.progress['temperature'] = temp
                logger.info("#########################")
                logger.info("Launch TestCases at {0} C".format(temp))
                logger.info("#########################")

                ######## Climatic Chamber ###################
                if self.cmd["climChamber"][0] == "yes":
                    self.clim.tempConsigne = temp
                    logger.info("Waiting for {0} seconds".format(self.scheduler['climChamberDelay']))
                    for remaining in range(self.scheduler['climChamberDelay'], 0, -1):
                        if not self.stopschedule:
                            logger.debug("{:2d} seconds remaining.".format(remaining))
                            time.sleep(1)
                        else:
                            self.progress['state'] = 0
                            self.progress['responseTask'] = 'abort'
                            logger.warning("Keyboard Interrupt. Stop countdown....")
                            self.clim.status = 0
                            return 'abort'
                    logger.info("\n")

                ############# Lance les thread pour chaque température ############
                for mode, tc in self.scheduler['tc2play'].items():
                    for tc_num in tc:
                        threadTc = TESTCASES[mode](temp=temp, simulate=self.simulate,
                                                   conf=self.cf.configs[mode][int(tc_num)],
                                                   comment=self.cmd["nameCarac"][0],
                                                   date=time.time(),
                                                   channel=self.dut_channel)

                        logger.info(
                            "Processing {0} -- Conf {1}/{2}".format(threadTc.__class__.__name__, int(tc_num) + 1,
                                                                    len(self.scheduler['tc2play'][mode])))
                        logger.info(time.strftime("%Y-%m-%d %H:%M:%S"))
                        bar = ProgressBar(threadTc.iterationsNumber, max_width=70)

                        # base de donnée
                        Progressbar.progress_value = threadTc.iterationsNumber

                        ## start threading
                        threadTc.tcInit()
                        threadTc.start()
                        current_iteration = threadTc.iteration

                        self.progress['tc_total'] = threadTc.iterationsNumber
                        nametc = list(threadTc.__class__.__name__) + list("-") + list(str(tc_num))
                        self.progress['tc'] = ''.join(nametc)
                        while threadTc.is_alive():
                            if not self.stopschedule:
                                time.sleep(0.1)
                                if threadTc.iteration != current_iteration:
                                    current_iteration = threadTc.iteration
                                    bar.numerator = current_iteration
                                    self.progress['current'] = step + current_iteration
                                    self.progress['tc_current'] = current_iteration
                                    if int(bar.percent % 20) == 0:
                                        logger.debug('{0}'.format(int(bar.percent)))
                            else:
                                self.progress['state'] = 0
                                self.progress['responseTask'] = 'abort'
                                logger.warning("Keyboard Interrupt Aborting ..... : threadTc was alive {0}".format(
                                    threadTc.__class__.__name__))
                                threadTc.abort()
                                threadTc.join()
                                if self.cmd["climChamber"][0] == "yes":
                                    self.clim.status = 0
                                logger.warning('carac abort')
                                return 'abort'

                        # progression backend
                        step = step + current_iteration
            logger.info("TestCases finished")
            if self.cmd["climChamber"][0] == "yes":
                logger.info("Switch off climatic chamber")
                self.clim.status = 0
            logger.info(time.strftime("%Y-%m-%d %H:%M:%S"))
            logger.info('carac succed ')
            self.progress['responseTask'] = 'success'
            return 'success'
        else:
            print("INPUT ERROR : commands are not valide")
