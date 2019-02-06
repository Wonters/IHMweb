#!/usr/bin/python3.7
# coding=UTF-8

import argparse
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.Swtch import *
from acbbs.drivers.dut import Dut
from acbbs.tools.log import get_logger, AcbbsError

import time

def test_ClimCham(simulate):
    clim = ClimCham(simulate=simulate)
    clim.tempConsigne = 25
    print("status : {0}".format(clim.status))
    print("tempConsigne : {0}".format(clim.tempConsigne))
    print("tempReal : {0}".format(clim.tempReal))
    print("info : {0}".format(clim.info))
    print("errors : {0}".format(clim.errors))
    clim.status = 1
    time.sleep(5)
    clim.status = 0

def test_PwrMeter(simulate):
    SpecAna = SpecAn(simulate=simulate)
    # SpecAna.reset()
    SpecAna.freqCenter = 902000000
    SpecAna.freqSpan = 100000000
    SpecAna.rbw = 10000
    SpecAna.vbw = 10000
    SpecAna.sweep = 0.1
    SpecAna.limitLineHSet(power = -50)
    SpecAna.averageCount(10)
    # SpecAna.limitSet(freq = [80000000, 940000000], power = [-20, -20])
    pwr = PwrMeter(simulate=simulate)
    pwr.reset()
    pwr.freq = 1000000000
    print("status : {0}".format(pwr.status))
    print("freq : {0}".format(pwr.freq))
    print("power : {0}".format(pwr.power))

def test_DCPwr(simulate):
    ### DCPwr test ###
    alim = DCPwr(simulate=simulate)
    alim.setChan(dutChan = 1)
    alim.reset()
    for i in range(1, 9):
        alim.setChan(dutChan = i)
        alim.status = 0
        alim.current = 6
        print("Channel {0}".format(i))
        print("status : {0}".format(alim.status))
        print("currentConsigne : {0}".format(alim.currentConsigne))
        print("currentReal : {0}".format(alim.currentReal))
        print("voltageConsigne : {0}".format(alim.voltageConsigne))
        print("voltageReal : {0}".format(alim.voltageReal))
        print("errors : {0}".format(alim.errors))
        print("")
    ##################

def test_SpecAna(simulate):
    ### RFSigGen test ###
    SpecAna = SpecAn(simulate=simulate)
    SpecAna.reset()
    SpecAna.freqCenter = 902000000
    SpecAna.freqSpan = 100000000
    SpecAna.freqStart = 902000000
    SpecAna.freqStop = 904000000
    SpecAna.rbw = 10000
    SpecAna.vbw = 10000
    SpecAna.refLvl = 10
    SpecAna.refLvlOffset = 10
    SpecAna.inputAtten = 20
    SpecAna.sweep = 1
    SpecAna.averageCount(2)
    SpecAna.limitSet(freq = [80000000, 940000000], power = [-20, -20])
    SpecAna.refreshDisplay()
    SpecAna.maxHoldCount(10)
    SpecAna.runSingle()
    SpecAna.markerSet(freq= 902100000)
    SpecAna.markerSearchLimit(freqleft=902101000, freqright=902102000)
    SpecAna.markerDelta()
    SpecAna.limitLineHSet(power=10, status=1)
    SpecAna.limitLineVSet(freq=902100000, status=1)
    SpecAna.limitSet(freq=[902100000], power=[10], margin=3)
    SpecAna.limitState(status=1)
    
    print("Info : {}".format(SpecAna.info))
    print("Max peak freq :{0}, value : {1}".format(SpecAna.markerPeakSearch()[0], SpecAna.markerPeakSearch()[1]))
    print("version : {0}".format(SpecAna.version))
    print("errors : {0}".format(SpecAna.errors))
    print("freqCenter : {0}".format(SpecAna.freqCenter))
    print("freqStart : {0}".format(SpecAna.freqStart))
    print("freqStop : {0}".format(SpecAna.freqStop))
    print("freqSpan : {0}".format(SpecAna.freqSpan))
    print("refLvl : {0}".format(SpecAna.refLvl))
    print("refLvlOffset : {0}".format(SpecAna.refLvlOffset))
    print("inputAtten : {0}".format(SpecAna.inputAtten))
    print("rbw : {0}".format(SpecAna.rbw))
    print("vbw : {0}".format(SpecAna.vbw))
    print("sweep : {0}".format(SpecAna.sweep))
    print("Marker Peak Search = {}".format(SpecAna.markerPeakSearch()))
    print("Marker Search = {}".format(SpecAna.markerSearch(dir='r')))
    print("Marker Get = {}".format(SpecAna.markerGet()))
    print("Limit check = {}".format(SpecAna.limitCheck()))
    #####################

def test_RFSigGen(simulate):
    ### RFSigGen test ###
    sigGen = RFSigGen(simulate=simulate)
    # sigGen.freq = 868525117
    sigGen.reset()
    sigGen.power = -100
    # sigGen.status = 1
    print("status : {0}".format(sigGen.status))
    print("power : {0}".format(sigGen.power))
    print("freq : {0}".format(sigGen.freq))
    print("version : {0}".format(sigGen.version))
    print("errors : {0}".format(sigGen.errors))
    #####################

def test_Swtch(simulate):
    ### Swtch test ###
    swtch = Swtch(simulate=simulate)
    swtch.setSwitch(sw1 = 1, sw2 = 1, sw3 = 4, sw4 = 2)
    swtch.setSwitch(sw1 = 1, sw2 = 1, sw3 = 2, sw4 = 2)
    swtch.setSwitch(sw1 = 1, sw2 = 1, sw3 = 4, sw4 = 1)
    swtch.setSwitch(sw1 = 1, sw2 = 1, sw3 = 3, sw4 = 2)
    ##################

def test_dut(simulate):
    ### dut test ###
    for i in range(1, 9):
        dutClass = Dut(chan=i, simulate=simulate)
        print("Channel {0} -> id : {1}".format(i, dutClass.tapId))
    ################

def main(args):
    test_DCPwr(args.simulate)
    test_RFSigGen(args.simulate)
    test_Swtch(args.simulate)
    test_dut(args.simulate)
    test_SpecAna(args.simulate)
    test_PwrMeter(args.simulate)
    test_ClimCham(args.simulate)

    logger = get_logger("test_coverage")
    logger.info("test")
    logger.debug("test")
    logger.warning("test")
    logger.error("test")
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "coverage test",
        fromfile_prefix_chars = '@' )
    parser.add_argument(
        "--simulate",
        help="play coverage in simulation",
        required = False,
        action="store_true")
    args = parser.parse_args()

    main(args)
