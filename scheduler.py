#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *
from acbbs.testcases.rxGainLNAs import *

import time
from progress.bar import PixelBar

def main(args):
    # threadSkeletonTc = skeletonTc()
    threadrxGainLNA = rxGainLNAs()

    bar = PixelBar('Processing rxGainLNAs', max=threadrxGainLNA.iterationsNumber)

    threadrxGainLNA.tcInit()
    threadrxGainLNA.start()

    i = threadrxGainLNA.iteration
    while threadrxGainLNA.is_alive():
        if threadrxGainLNA.iteration != i:
            i = threadrxGainLNA.iteration
            bar.next()
    bar.finish()


    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
