#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *
from acbbs.testcases.rxGainLNA import *

import time
from progress.bar import Bar

def main(args):
    threadSkeletonTc = skeletonTc()
    threadrxGainLNA = rxGainLNA()
    # threadrxGainLNA.tcInit()
    # threadrxGainLNA.start()

    bar = Bar('Processing', max=threadSkeletonTc.iterationsNumber)
    i = threadSkeletonTc.iteration

    threadSkeletonTc.tcInit()
    threadSkeletonTc.start()
    while threadSkeletonTc.is_alive():
        if threadSkeletonTc.iteration != i:
            i = threadSkeletonTc.iteration
            bar.next()
    bar.finish()


    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
