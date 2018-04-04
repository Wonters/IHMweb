#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.rxGainLNAs import *
from acbbs.testcases.rxIQImbalance import *
from acbbs.testcases.rxP1dBSaturation import *
from acbbs.testcases.rxMaximumGain import *

from acbbs.drivers.ate.ClimCham import *

import time
from progress.bar import PixelBar

def main(args):

    #get configuration
    conf = configurationFile(file = self.__class__.__name__)
    schConf = conf.getConfiguration()

    #start loops
    for temp in schConf["temperature"]:
        #set temperature and wait

        for tc in schConf["tc2play"]:
            cmd = "threadTc = {0}()".format(tc)
            exec cmd

            bar = PixelBar("Processing {0}".format(tc), max=threadTc.iterationsNumber)

            threadTc.tcInit()
            threadTc.start()

            i = threadTc.iteration
            while threadTc.is_alive():
                time.sleep(0.1)
                if threadTc.iteration != i:
                    i = threadTc.iteration
                    bar.next()
            bar.finish()

    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
