#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.dut import *

def test_DCPwr():
    ### DCPwr test ###
    alim = DCPwr()
    for i in range(1, 9):
        alim.setChan(dutChan = i)
        print("Channel {0}".format(i))
        print("status : {0}".format(alim.status))
        print("currentConsigne : {0}".format(alim.currentConsigne))
        print("currentReal : {0}".format(alim.currentReal))
        print("voltageConsigne : {0}".format(alim.voltageConsigne))
        print("voltageReal : {0}".format(alim.voltageReal))
        print("errors : {0}".format(alim.errors))
        print("")
    ##################

def test_RFSigGen():
    sigGen = RFSigGen()
    # sigGen.freq = 868525117
    # sigGen.power = -100
    sigGen.reset()
    print("status : {0}".format(sigGen.status))
    print("power : {0}".format(sigGen.power))
    print("freq : {0}".format(sigGen.freq))
    print("version : {0}".format(sigGen.version))
    print("errors : {0}".format(sigGen.errors))

def main(args):
    # test_DCPwr()
    test_RFSigGen()
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
