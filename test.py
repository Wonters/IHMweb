#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.Swtch import *
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
    ### RFSigGen test ###
    sigGen = RFSigGen()
    # sigGen.freq = 868525117
    # sigGen.power = -100
    sigGen.status = 1
    print("status : {0}".format(sigGen.status))
    print("power : {0}".format(sigGen.power))
    print("freq : {0}".format(sigGen.freq))
    print("version : {0}".format(sigGen.version))
    print("errors : {0}".format(sigGen.errors))
    #####################

def test_Swtch():
    ### Swtch test ###
    swtch = Swtch()
    swtch.setSwitch(sw1 = 1, sw2 = None, sw3 = None, sw4 = None)
    ##################

def test_dut():
    ### dut test ###
    for i in range(1, 9):
        dutClass = dut(chan=i)
        print("Channel {0} -> id : {1}".format(i, dutClass.tapId))
    ################

def test_rssiSin():
    ### dut test ###
    dutClass = dut(chan=1)
    dutClass.mode = "RX"
    dutClass.preamp0 = "LNA"
    dutClass.preamp1 = "LNA"
    dutClass.preamp2 = "LNA"
    dutClass.freqRx = 902200000

    swtch = Swtch()
    swtch.setSwitch(sw1 = 1, sw2 = 4, sw3 = 3, sw4 = 1)

    sigGen = RFSigGen()
    sigGen.power = -70
    sigGen.freq = 902220000
    sigGen.status = 1
    ref = dutClass.rssiSin()
    print("dutClass.rssiSin() return {0}".format(ref))
    ################

def main(args):
    test_DCPwr()
    # test_RFSigGen()
    # test_Swtch()
    # test_dut()
    # test_rssiSin()
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
