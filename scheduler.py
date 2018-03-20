#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *
from acbbs.testcases.rxGainLNAs import *
from acbbs.testcases.rxIQImbalance import *

import time
from progress.bar import PixelBar

def main(args):
    # threadSkeletonTc = skeletonTc()
    # threadTc = rxGainLNAs()
    threadTc = rxIQImbalance()

    bar = PixelBar('Processing rxGainLNAs', max=threadTc.iterationsNumber)

    threadTc.tcInit()
    threadTc.start()

    i = threadTc.iteration
    while threadTc.is_alive():
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
