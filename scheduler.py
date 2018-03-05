#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *
from acbbs.testcases.rxGainLNA import *

import time

def main(args):
    threadSkeletonTc = skeletonTc()
    threadSkeletonTc.tcInit()
    # threadSkeletonTc.start()
    threadrxGainLNA = rxGainLNA()
    threadrxGainLNA.tcInit()
    threadrxGainLNA.start()

    while threadrxGainLNA.is_alive():
        # if threadGenericTc.getProgress() > 40 :
        #     threadGenericTc.abort()
        print("progress : {0:.2f} Status = {1}".format(threadrxGainLNA.getProgress(), threadrxGainLNA.getStatus()))
        time.sleep(0.5)

    print("progress : {0:.2f} Status = {1}".format(threadrxGainLNA.getProgress(), threadrxGainLNA.getStatus()))

    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
