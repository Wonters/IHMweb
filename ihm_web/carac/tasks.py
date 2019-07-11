from __future__ import absolute_import, unicode_literals

import time

from acbbs.drivers.ate.ClimCham import ClimCham
from acbbs.tools.log import get_logger

from etaprogress.progress import ProgressBar

import configuration

from .models import Progressbar,Campagnmodel

## ajouter la lib du nouveau testcase ici ##


log = get_logger("task")

## ajouter la lib à l'intèrieure du tableau ##
TESTCASES = configuration.TESTCASES


class TaskScheduler:

    def __init__(self, conf, command, scheduler):
        self.stopschedule = bool
        self.cmd = command
        self.cf = conf
        self.threadTc_list = []
        self.scheduler = scheduler

        self.initializeProgress()
        self.initializeCampagn()

        self.comment = ""

    def initializeProgress(self):
        Progressbar.current = 0
        Progressbar.total = 0
        Progressbar.state = 0
        Progressbar.temperature = 0
        Progressbar.responseTask = 'ready'
        Progressbar.tc_total = 0
        Progressbar.tc_current = 0
        Progressbar.tc = ''

    def initializeCampagn(self):
        Campagnmodel.campagn_channels = ''
        Campagnmodel.campagn_climChamber = 0
        Campagnmodel.campagn_date = ''
        Campagnmodel.campagn_type = ''
        Campagnmodel.campagn_name = ''
        Campagnmodel.campagm_clim_current = 0
        Campagnmodel.campagn_clim_total = 0
        Campagnmodel.campagn_tc2play = ''
        Campagnmodel.campagn_templist = ''


    def get_cmd(self):
        log.debug("{0}".format(self.cmd))
        if self.cmd:
            self.cmd['configFile'] = self.cf.nameConf

            if self.cmd["simulate"][0] == "yes":
                log.info("simulate")
                self.simulate = True
            else:
                self.simulate = False
                log.info("no simulate")
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
            log.debug('simulate:{0}, climChamber:{1},channels: {2}'.format(self.simulate, self.cmd["climChamber"][0],
                                                                              self.dut_channel))
            self.comment = self.cmd["nameCarac"] + "_" + time.strftime("%Y-%m-%d %H:%M:%S")

            # Enregistrement dans la base de donnée Django de la campagne lancée
            Campagnmodel.campagn_channels = self.cmd["channel"][0]
            Campagnmodel.campagn_climChamber = self.cmd["climChamber"][0]
            Campagnmodel.campagn_date = time.strftime("%Y-%m-%d %H:%M:%S")
            Campagnmodel.campagn_type = self.cmd["nameCarac"]
            Campagnmodel.campagn_name = self.cmd["configFile"]
            Campagnmodel.campagn_clim_total = self.scheduler["climChamberDelay"]
            Campagnmodel.campagn_templist = self.scheduler["temperature"]
            return True
        else:
            log.debug('commands are not valide')
            return False

    def get_totalProgress(self):
        tc2play = ''
        if Progressbar.total == 0:
            self.threadTc_list = []
            for mode, tc in self.scheduler['tc2play'].items():
                for tc_num in tc:
                    self.threadTc_list.append(TESTCASES[mode](temp=0, simulate=True,
                                                              conf=self.cf.configs[mode][int(tc_num)],
                                                              comment=self.cmd["nameCarac"],
                                                              date=time.time(),
                                                              channel=self.dut_channel))
                    if self.cf.configs[mode][int(tc_num)]["name"] == "":
                        tc2play = tc2play + mode + "-" + str(tc_num) + ","
                    else:
                        tc2play = tc2play + self.cf.configs[mode][int(tc_num)]["name"] + ","
            for threadTc in self.threadTc_list:
                Progressbar.total = Progressbar.total + threadTc.iterationsNumber
            Progressbar.total = Progressbar.total * len(self.scheduler['temperature'])
            Campagnmodel.campagn_tc2play = tc2play

    # lance la caractérisation, dépend de la class caracatérisation
    def start(self):
        self.stopschedule = 0
        # tampon qui stocke les itération successive entre chaque tc
        step = 0
        if self.get_cmd() is True:
            # init progress backend
            self.get_totalProgress()

            log.info("carac start ....")
            Progressbar.responseTask = 'running'
            Progressbar.state = 1

            ######### LOOP ###################
            for temp in self.scheduler['temperature']:
                Progressbar.temperature = temp
                log.info("#########################")
                log.info("Launch TestCases at {0} C".format(temp))
                log.info("#########################")

                ######## Climatic Chamber ###################
                if self.cmd["climChamber"][0] == "yes":
                    self.clim.tempConsigne = temp
                    log.info("Waiting for {0} seconds".format(self.scheduler['climChamberDelay']))
                    for remaining in range(self.scheduler['climChamberDelay'], 0, -1):
                        if not self.stopschedule:
                            log.debug("{:2d} seconds remaining.".format(remaining))
                            Campagnmodel.campagm_clim_current = self.scheduler["climChamberDelay"] - remaining + 1
                            time.sleep(1)
                        else:
                            Progressbar.state = 0
                            Progressbar.responseTask = 'abort'
                            log.warning("Keyboard Interrupt. Stop countdown....")
                            self.clim.status = 0
                            return 'abort'
                    log.info("\n")

                ############# Lance les thread pour chaque température ############
                for mode, tc in self.scheduler['tc2play'].items():
                    for tc_num in tc:
                        threadTc = TESTCASES[mode](temp=temp, simulate=self.simulate,
                                                   conf=self.cf.configs[mode][int(tc_num)],
                                                   comment=self.comment,
                                                   date=time.time(),
                                                   channel=self.dut_channel)

                        log.info("Processing {0} -- Conf {1}/{2}".format(threadTc.__class__.__name__, int(tc_num) + 1,
                                                                    len(self.scheduler['tc2play'][mode])))
                        log.info(time.strftime("%Y-%m-%d %H:%M:%S"))
                        bar = ProgressBar(threadTc.iterationsNumber, max_width=70)

                        # base de donnée
                        #Progressbar.progress_value = threadTc.iterationsNumber


                        ## start threading
                        threadTc.tcInit()
                        threadTc.start()
                        current_iteration = threadTc.iteration

                        Progressbar.tc_total = threadTc.iterationsNumber
                        if self.cf.configs[mode][int(tc_num)]['name'] == '':
                            nametc = list(threadTc.__class__.__name__) + list("-") + list(str(tc_num))
                            Progressbar.tc = ''.join(nametc)
                        else:
                            Progressbar.tc = self.cf.configs[mode][int(tc_num)]['name']

                        while threadTc.is_alive():
                            if not self.stopschedule:
                                time.sleep(0.1)
                                if threadTc.iteration != current_iteration:
                                    current_iteration = threadTc.iteration
                                    bar.numerator = current_iteration
                                    Progressbar.current = step + current_iteration
                                    Progressbar.tc_current = current_iteration
                                    if int(bar.percent % 20) == 0:
                                        log.debug('{0}'.format(int(bar.percent)))
                            else:
                                Progressbar.state = 0
                                Progressbar.responseTask = 'abort'
                                log.warning("Keyboard Interrupt Aborting ..... : threadTc was alive {0}".format(
                                    threadTc.__class__.__name__))
                                threadTc.abort()
                                threadTc.join()
                                if self.cmd["climChamber"][0] == "yes":
                                    self.clim.status = 0
                                log.warning('carac abort')
                                return 'abort'

                        # progression backend
                        step = step + current_iteration
            log.info("TestCases finished")
            if self.cmd["climChamber"][0] == "yes":
                log.info("Switch off climatic chamber")
                self.clim.status = 0
            log.info(time.strftime("%Y-%m-%d %H:%M:%S"))
            log.info('carac succed ')
            Progressbar.responseTask = 'success'
            return 'success'
        else:
            print("INPUT ERROR : commands are not valide")
