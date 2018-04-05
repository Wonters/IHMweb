#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.rxGainLNAs import *
from acbbs.testcases.rxIQImbalance import *
from acbbs.testcases.rxP1dBSaturation import *
from acbbs.testcases.rxMaximumGain import *

from acbbs.drivers.ate.ClimCham import *

import time
import sys
from progress.bar import PixelBar

def main(args):
    #get configuration
    conf = configurationFile(file = "scheduler")
    schConf = conf.getConfiguration()
    if schConf["simulate"] == "True":
        simulate = True
    else:
        simulate = False

    #start loops
    for temp in schConf["temperature"]:
        #set temperature and wait

        for tc in schConf["tc2play"]:
            exec "threadTc = {0}(temp={1}, simulate={2})".format(tc, temp, simulate)

            bar = PixelBar("Processing {0}".format(tc), max=threadTc.iterationsNumber)

            threadTc.tcInit()
            threadTc.start()

            i = threadTc.iteration
            try:
                while threadTc.is_alive():
                    time.sleep(0.1)
                    if threadTc.iteration != i:
                        i = threadTc.iteration
                        bar.next()
                bar.finish()

            except KeyboardInterrupt:
                print("\nKeyboard Interrupt Aborting....")
                threadTc.abort()
                threadTc.join()
                sys.exit(0)

    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
