#!/usr/bin/python2.7
# coding=UTF-8

import argparse
from acbbs.drivers.ate.ClimCham import *
from acbbs.drivers.ate.DCPwr import *
from acbbs.drivers.ate.PwrMeter import *
from acbbs.drivers.ate.RFSigGen import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.Swtch import *
from acbbs.drivers.dut import Dut

import time

def test_ClimCham():
    clim = ClimCham(simulate=False)
    clim.tempConsigne = 25
    print("status : {0}".format(clim.status))
    print("tempConsigne : {0}".format(clim.tempConsigne))
    print("tempReal : {0}".format(clim.tempReal))
    clim.status = 1
    time.sleep(5)
    clim.status = 0

def test_PwrMeter():
    SpecAna = SpecAn()
    # SpecAna.reset()
    SpecAna.freqCenter = 902000000
    SpecAna.freqSpan = 100000000
    SpecAna.rbw = 10000
    SpecAna.vbw = 10000
    SpecAna.sweep = 0.1
    SpecAna.limitLineHSet(power = -50)
    SpecAna.averageCount(10)
    # SpecAna.limitSet(freq = [80000000, 940000000], power = [-20, -20])
    pwr = PwrMeter()
    pwr.freq = 1000000000
    print("status : {0}".format(pwr.status))
    print("freq : {0}".format(pwr.freq))
    print("power : {0}".format(pwr.power))

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

def test_SpecAna():
    ### RFSigGen test ###
    SpecAna = SpecAn()
    # SpecAna.reset()
    SpecAna.freqCenter = 902000000
    SpecAna.freqSpan = 100000000
    SpecAna.rbw = 10000
    SpecAna.vbw = 10000
    SpecAna.sweep = 1
    SpecAna.averageCount(2)
    SpecAna.limitSet(freq = [80000000, 940000000], power = [-20, -20])
    # SpecAna.freqStart = 902000000
    # SpecAna.freqStop = 904000000
    # print("power : {0}".format(sigGen.power))
    # print("freq : {0}".format(sigGen.freq))
    print("Max peak freq :{0}, value : {1}".format(SpecAna.markerPeakSearch()[0], SpecAna.markerPeakSearch()[1]))
    print("version : {0}".format(SpecAna.version))
    print("errors : {0}".format(SpecAna.errors))
    print("freqCenter : {0}".format(SpecAna.freqCenter))
    print("freqStart : {0}".format(SpecAna.freqStart))
    print("freqStop : {0}".format(SpecAna.freqStop))
    print("freqSpan : {0}".format(SpecAna.freqSpan))
    print("rbw : {0}".format(SpecAna.rbw))
    print("vbw : {0}".format(SpecAna.vbw))
    print("inputAtten : {0}".format(SpecAna.inputAtten))
    print("refLvl : {0}".format(SpecAna.refLvl))
    print("refLvlOffset : {0}".format(SpecAna.refLvlOffset))
    print("sweep : {0}".format(SpecAna.sweep))
    #####################

def test_RFSigGen():
    ### RFSigGen test ###
    sigGen = RFSigGen()
    # sigGen.freq = 868525117
    sigGen.power = -100
    # sigGen.status = 1
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
        dutClass = Dut(chan=i)
        print("Channel {0} -> id : {1}".format(i, dutClass.tapId))
    ################

def test_rssiSin():
    ### dut test ###
    dutClass = Dut(chan=1)
    dutClass.mode = "RX"
    dutClass.preamp0 = "LNA"
    dutClass.preamp1 = "LNA"
    dutClass.preamp2 = "LNA"
    dutClass.freqRx = 902200000

    swtch = Swtch()
    swtch.setSwitch(sw1 = 1, sw2 = 4, sw3 = 3, sw4 = 1)

    sigGen = RFSigGen()
    sigGen.power = -60
    sigGen.freq = 902220000
    sigGen.status = 1
    ref = dutClass.rssiSin()
    # ref = dutClass.rssiSinNumpy()
    print("dutClass.rssiSin() return {0}".format(ref))
    ################

def test_rssiSinNumpy():
    ### dut test ###
    dutClass = Dut(chan=1)
    dutClass.mode = "RX"
    dutClass.preamp0 = "LNA"
    dutClass.preamp1 = "LNA"
    dutClass.preamp2 = "LNA"
    dutClass.freqRx = 902200000

    swtch = Swtch()
    swtch.setSwitch(sw1 = 1, sw2 = 4, sw3 = 3, sw4 = 1)

    sigGen = RFSigGen()
    sigGen.power = -60
    sigGen.freq = 902220000
    sigGen.status = 1
    print("dutClass.rssiSin() return {0}".format(ref))
    ################

def test_freqAcc():
    d = Dut(chan=1, simulate=False)
    s = SpecAn(simulate=False)

    inputAtt = 18
    span = 10000000
    refLvl = 42
    refLvlOffset = 24

    freq_tx_list = [869525000, 869527000]
    filter_tx = 1


    s.inputAtt = inputAtt
    s.freqSpan = span

    for freq_tx in freq_tx_list:

        d.mode = "TX"

        s.refLvlOffset = refLvlOffset
        s.refLvl = refLvl

        d.freqTx = freq_tx
        d.filterTx = filter_tx
        s.freqCenter = freq_tx

        d.playBBSine(freqBBHz = 0, atten = 28)

        s.freqSpan = 200000
        s._readWrite("CALC:MARK{0} ON".format(1))
        s._readWrite("CALC:MARK{0}:MAX".format(1))
        time.sleep(10)

        s._readWrite("CALC:MARK{0}:COUN ON".format(1))
        resultOLFrequency = float(s._readWrite("CALC:MARK{0}:COUN:FREQ?".format(1)))

        print("result = {}".format(resultOLFrequency))
        print("delta = {:.1f}".format(abs(resultOLFrequency-freq_tx)))

        d.stopBBSine()


def test_irrSin():
    ### dut test ###
    dutClass = Dut(chan=1)
    dutClass.mode = "RX"
    dutClass.preamp0 = "LNA"
    dutClass.preamp1 = "LNA"
    dutClass.preamp2 = "LNA"
    dutClass.freqRx = 902200000

    swtch = Swtch()
    swtch.setSwitch(sw1 = 1, sw2 = 4, sw3 = 3, sw4 = 1)

    sigGen = RFSigGen()
    sigGen.power = -60
    sigGen.freq = 902220000
    sigGen.status = 1
    # ref = dutClass.irrSin()
    ref = dutClass.rssiSinNumpy()
    # print("dutClass.rssiSin() return {0}".format(ref))
    ################

# import matplotlib.pyplot as plt
# from scipy.fftpack import fft
# from scipy.io import wavfile # get the api
def test_fft():
    fs, data = wavfile.read('test.wav') # load the data
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    b=[(ele/2**16.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # calculate fourier transform (complex numbers list)
    d = len(c)/2  # you only need half of the fft list (real signal symmetry)
    e = abs(c[:(d-1)])
    # plt.plot(e)

    peak = 0
    for i in e:
        if i > peak and i < 100000:
            peak = i
    print('Peaks are: %s' % (peak))

    # plt.show()

def main(args):
    # test_DCPwr()
    # test_RFSigGen()
    # test_Swtch()
    # test_dut()
    # test_rssiSin()
    # test_irrSin()
    # test_fft()
    # test_rssiSinNumpy()
    # test_SpsecAna()
    # test_PwrMeter()
    # test_ClimCham()
    test_freqAcc()
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Scheduler for acbbs",
        fromfile_prefix_chars = '@' )
    args = parser.parse_args()

    main(args)
