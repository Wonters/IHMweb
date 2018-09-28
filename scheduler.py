#!/usr/bin/python2.7
# coding=UTF-8

from __future__ import print_function
from etaprogress.progress import ProgressBar

from acbbs.drivers.ate.ClimCham import ClimCham

from acbbs.testcases.rxExcursion import rxExcursion

from acbbs.testcases.txExcursion import txExcursion
from acbbs.testcases.txIM3Measurement import txIM3Measurement
from acbbs.testcases.txSpurious import txSpurious

from acbbs.tools.configurationFile import configurationFile

import argparse
import time
import sys

def main(args):
    #print date
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

    #get configuration
    conf = configurationFile(file = "scheduler", taphw = args.dut)
    schConf = conf.getConfiguration()
    if schConf["simulate"] == "True":
        simulate = True
    else:
        simulate = False

    #start loops
    for temp in schConf["temperature"]:
        #set temperature and wait
        print("\n#########################")
        print("Launch TestCases at {0}C".format(temp))
        print("#########################\n")

        for tc in schConf["tc2play"]:
            exec "threadTc = {0}(temp={1}, simulate={2})".format(tc, temp, simulate)

            print("Processing {0}".format(tc))
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            bar = ProgressBar(threadTc.iterationsNumber, max_width=70)

            threadTc.tcInit()
            threadTc.start()

            i = threadTc.iteration
            try:
                while threadTc.is_alive():
                    time.sleep(0.1)
                    if threadTc.iteration != i:
                        i = threadTc.iteration
                        bar.numerator = i
                        print (bar, end='\r')
                        sys.stdout.flush()
                print("\n\n")

            except KeyboardInterrupt:
                print("\n\nKeyboard Interrupt Aborting....")
                threadTc.abort()
                threadTc.join()
                sys.exit(0)

    print("TestCases finished")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    exit(0)

if __name__ == '__main__':
    taplist = ["TAPMV3.0", "TAPMV4.0"]
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    parser.add_argument(
        "-d",
        "--dut",
        help="set type of DUT",
        required = True)
    args = parser.parse_args()
    main(args)
