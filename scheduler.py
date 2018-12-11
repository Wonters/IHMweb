#!/usr/bin/python2.7
# coding=UTF-8

from __future__ import print_function
from etaprogress.progress import ProgressBar

from acbbs.drivers.ate.ClimCham import ClimCham

from acbbs.testcases.rxExcursion import rxExcursion

from acbbs.testcases.txExcursion import txExcursion
from acbbs.testcases.txIM3Measurement import txIM3Measurement

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
    if args.simulate:
        simulate = True
    else:
        simulate = False

    print(simulate)

    try:
        dut_channel = args.channel.split(",")
        for i in range(0, len(dut_channel)):
            dut_channel[i] = int(dut_channel[i])
    except:
        print("Error parsing DUT channel")
        exit(0)

    #initialize climatic chamber
    if args.noclimchamb is False:
        clim = ClimCham(simulate=simulate)
        clim.status = 1

    #start loops
    for temp in schConf["temperature"]:
        #set temperature and wait
        print("\n#########################")
        print("Launch TestCases at {0}C".format(temp))
        print("#########################\n")

        if args.noclimchamb is False:
            print("Set climatic chamber at {0} C".format(temp))
            clim.tempConsigne = temp
            print("Waiting for {0} seconds".format(schConf["climChamberDelay"]))
            try:
                for remaining in range(schConf["climChamberDelay"], 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
                    sys.stdout.flush()
                    time.sleep(1)

            except KeyboardInterrupt:
                print("\n\nKeyboard Interrupt. Stop countdown....")
                clim.status = 0
                sys.exit(0)


            print("\n")

        for tc in schConf["tc2play"]:
            for conf_number in range (0, len(conf.getConfiguration(file=tc))):
                exec "threadTc = {0}(temp={1}, simulate={2}, conf={3}, comment=\"{4}\", date={5}, channel={6})".format(tc, temp, simulate, conf.getConfiguration(file=tc)[conf_number], args.comment, time.time(), dut_channel)

                print("Processing {0} -- Conf {1}/{2}".format(tc, conf_number + 1, len(conf.getConfiguration(file=tc))))
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
                    if args.noclimchamb is False:
                        clim.status = 0
                    sys.exit(0)

    print("TestCases finished")
    if args.noclimchamb is False:
        print("Switch off climatic chamber")
        clim.status = 0
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    exit(0)

if __name__ == '__main__':
    taplist = ["TAPV3.0", "TAPMV4.0"]
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    parser.add_argument(
        "-d",
        "--dut",
        help="set type of DUT. Use configuration_assistant.py -l to list DUT",
        required = True)
    parser.add_argument(
        "-m",
        "--comment",
        help="set comment for this measure",
        required = True)
    parser.add_argument(
        "--simulate",
        help="play testcases in simulation",
        required = False,
        action="store_true")
    parser.add_argument(
        "--noclimchamb",
        help="disable climatic chamber",
        required = False,
        action="store_true")
    parser.add_argument(
        "--channel",
        help="set DUT channel separate by comma (ex: 1,2,3,4,5,6,7,8)",
        required = True,)
    args = parser.parse_args()
    main(args)
