#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.rxGainLNAs import *

def main(args):
    tcGainLNAs = rxGainLNAs()
    tcGainLNAsrxProgress = tcGainLNAs.getProgress()
    tcGainLNAs.run()
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
