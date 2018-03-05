#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.testcases.skeletonTc import *

import time

def main(args):
    threadSkeletonTc = skeletonTc()
    threadSkeletonTc.tcInit()
    exit(0)
    threadSkeletonTc.start()

    while threadSkeletonTc.is_alive():
        # if threadGenericTc.getProgress() > 40 :
        #     threadGenericTc.abort()
        print("progress : {0:.2f} Status = {1}".format(threadSkeletonTc.getProgress(), threadSkeletonTc.getStatus()))
        time.sleep(0.5)

    print("progress : {0:.2f} Status = {1}".format(threadSkeletonTc.getProgress(), threadSkeletonTc.getStatus()))

    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
