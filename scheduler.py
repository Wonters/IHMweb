#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *
from acbbs.testcases.rxGainLNAs import *

import time
from progress.bar import PixelBar

def main(args):
    # threadSkeletonTc = skeletonTc()
    threadrxGainLNAs = rxGainLNAs()

    bar = PixelBar('Processing rxGainLNAs', max=threadrxGainLNAs.iterationsNumber)

    threadrxGainLNAs.tcInit()
    threadrxGainLNAs.start()

    i = threadrxGainLNAs.iteration
    while threadrxGainLNAs.is_alive():
        if threadrxGainLNAs.iteration != i:
            i = threadrxGainLNAs.iteration
            bar.next()
    bar.finish()


    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
