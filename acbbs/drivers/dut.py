# coding=UTF-8
from ..tools.log import get_logger, AcbbsError, log

import requests
import os
import sys

import subprocess
import time

import math

import numpy as np

from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from scipy import signal

folder = os.path.dirname(os.path.abspath(__file__))
#Set log class in connectionpool Class with the CustomLog class
requests.packages.urllib3.connectionpool.log.__class__ = log
#Rename log name
requests.packages.urllib3.connectionpool.log.name = "connectionPool"

TIMEOUT = 5

class Dut(object):
    class _simulate(object):
        class post(object):
            def __init__(self, uri, json=None, timeout=None, auth=None):
                pass

            @property
            def status_code(self):
                return 200

        class get(object):
            def __init__(self, uri, auth=None, stream=None, timeout=None):
                pass

            def iter_content(self, chunk_size=None):
                pass

            def json(self):
                return {
                    "preamp":"xxxx",
                    "tapid":"xxxx",
                    "taphw":"xxxx",
                    "tapsw":"xxxx",
                    "radiohw":"xxxx",
                    "radiofw":"xxxx",
                    "tpmhw":"xxxx",
                    "tpmVendor":"xxxx",
                    "measures":"xxxx",
                    "tx":"xxxx",
                    "rx":"xxxx",
                    "mode":"xxxx"
                    }

            @property
            def status_code(self):
                return 200

        def __init__(self):
            pass

    def __init__(self , chan=None, ip=None, simulate = False):
        '''
        Constructor
        '''
        #init logs
        self.logger = get_logger(self.__class__.__name__)

        if ip is None and chan is None:
            raise AcbbsError("Ip or Channel mandatory", log=self.logger)

        #simulation state
        self.simulate = simulate

        #case of simulate
        if simulate :
            self.logger.info("Init dut in Simulate")
            self.session = self._simulate()

        else :
            self.logger.info("Init dut")
            self.session = requests.Session()
        
        if chan is not None:
            self.channel = chan
            self.address = "http://192.168.%s.128/factory" % str(chan)
        if ip is not None:
            self.channel = ip
            self.address = "http://%s/factory" % ip
        
        self.logger.info("New RadioDevice %s" % (self.address), ch=self.channel)

        self.tapId_var = None
        self.tapHw_var = None
        self.tapSw_var = None
        self.radioHw_var = None
        self.radioFw_var = None
        self.tpmHw_var = None
        self.tpmVendor_var = None

        self.logger.info("Check dut-ip : {0}".format(chan), ch = chan)
        if self.connected:
            self.logger.info("DUT at {0} well connected".format(chan), ch = chan)
        else:
            raise AcbbsError("Connection Errors", ch=self.channel, log=self.logger)
        if self.tapHw == "TAPMV4.0":
		    self.preamp1 = "LNA"

    def __del__(self):
        self.logger.info("dut off")
        self.stopBBSine()
        self.stopBBNoise()
        self.mode = "RX"

    def _launchCmd(self, uri, get = True, payloadJson = None, payloadData = None, stream = False, callback = None):
        if get:
            resp = self.session.get(uri, auth=('factory', 'factory'), stream=stream, timeout=TIMEOUT)
            self.logger.debug("GET %s %s" % (uri , resp.status_code), ch=self.channel)
            if stream :
                if "signal/record" not in uri:
                    raise AcbbsError("Stream is compatible only with signal/record request",
                                      ch=self.channel, log=self.logger)
                if callback is None:
                    raise AcbbsError("Stream activate but there is no callback",
                                     ch=self.channel, log=self.logger)
                nbChunk = 0
                ret = 0
                stoped = 0
                for chunk in resp.iter_content(chunk_size=2048):
                    nbChunk = nbChunk + len(chunk)
                    if stoped is 0:
                        if ret is not 0:
                            self.session.post("%s/signal/stop" % self.address)
                            stoped = 1
                        else:
                            ret = callback(resp, chunk)
            if resp.status_code not in [200, 204, 201]:
                if resp.status_code == 500:
                    raise AcbbsError("Bad status code %u for GET on %s dump %s" %
                                     (resp.status_code, uri, self._dumpErrors()), ch=self.channel, log=self.logger)
                else:
                    raise AcbbsError("Bad status code %u for GET on %s" % (resp.status_code, uri),
                                     ch=self.channel, log=self.logger)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 204:
                return nbChunk

        else:
            if payloadJson:
                resp = self.session.post(uri, json=payloadJson, timeout=TIMEOUT, auth=('factory', 'factory'))
            elif payloadData:
                resp = self.session.post(uri, data=payloadData, headers={'Content-Type': 'application/octet-stream'}, timeout=TIMEOUT, auth=('factory', 'factory'))
            else:
                resp = self.session.post(uri, timeout=TIMEOUT, auth=('factory', 'factory'))
            self.logger.debug("POST %s %s" % (uri , resp.status_code), ch=self.channel)
            if resp.status_code not in [200, 204]:
                if resp.status_code == 500:
                    raise AcbbsError("Bad status code %u for POST on %s dump %s" %
                                     (resp.status_code, uri, self._dumpErrors()), ch=self.channel, log=self.logger)
                else:
                    raise AcbbsError("Bad status code %u for POST on %s" % (resp.status_code, uri),
                                      ch=self.channel, log=self.logger)

    def _launchGetJson(self, uri):
        return self._launchCmd(uri, True, None, None, False, None)
    def _launchGetStream(self, uri, callback=None):
        return self._launchCmd(uri, True, None, None, True, callback)
    def _launchPost(self, uri):
        return self._launchCmd(uri, False, None, None, False, None)
    def _launchPostJson(self, uri, payloadJson=None):
        return self._launchCmd(uri, False, payloadJson, None, False, None)
    def _launchPostData(self, uri, payloadData=None):
        return self._launchCmd(uri, False, None, payloadData, False, None)

    @property
    def info(self):
        return {
            "id":self.tapId,
            "tap-hw":self.tapHw,
            "tap-sw":self.tapSw,
            "radio-hw":self.radioHw,
            "radio-fw":self.radioFw,
            "tpm-hw":self.tpmHw,
            "tpm-vendor":self.tpmVendor,
            "freq-tx":self.freqTx,
            "freq-rx":self.freqRx,
            "mode":self.mode,
            "preamp0":self.preamp0,
            "preamp1":self.preamp1,
            "preamp2":self.preamp2,
            "measure":self.allMeasure
        }

    @property
    def connected(self):
        try:
            self._launchGetJson("%s/info" % self.address)
        except:
            return False
        else:
            return True

    @property
    def tapId(self):
        if self.tapId_var is None:
            if self.simulate:
                self.tapId_var = "xxxx"
            else:
                self.tapId_var = self._launchGetJson("%s/info" % self.address)['tapid']
        return self.tapId_var

    @property
    def tapHw(self):
        if self.tapHw_var is None:
            if self.simulate:
                self.tapHw_var = "xxxx"
            else:
                self.tapHw_var = self._launchGetJson("%s/info" % self.address)['taphw']
        return self.tapHw_var

    @property
    def tapSw(self):
        if self.tapSw_var is None:
            if self.simulate:
                self.tapSw_var = "xxxx"
            else:
                self.tapSw_var = self._launchGetJson("%s/info" % self.address)['tapsw']
        return self.tapSw_var

    @property
    def radioHw(self):
        if self.radioHw_var is None:
            if self.simulate:
                self.radioHw_var = "xxxx"
            else:
                self.radioHw_var = self._launchGetJson("%s/info" % self.address)['radiohw']
        return self.radioHw_var

    @property
    def radioFw(self):
        if self.radioFw_var is None:
            if self.simulate:
                self.radioFw_var = "xxxx"
            else:
                self.radioFw_var = self._launchGetJson("%s/info" % self.address)['radiofw']
        return self.radioFw_var

    @property
    def tpmHw(self):
        if self.tpmHw_var is None:
            if self.simulate:
                self.tpmHw_var = "xxxx"
            else:
                self.tpmHw_var = self._launchGetJson("%s/info" % self.address)['tpmhw']
        return self.tpmHw_var

    @property
    def tpmVendor(self):
        if self.tpmVendor_var is None:
            if self.simulate:
                self.tpmVendor_var = "xxxx"
            else:
                self.tpmVendor_var = self._launchGetJson("%s/info" % self.address)['tpmvendor']
        return self.tpmVendor_var

    @property
    def allMeasureAvailable(self):
        listAvailable = self._launchGetJson("%s/measures" % (self.address))['measures']
        if self.tapHw == "TAPMV4.0":
            listAvailable.extend(self._launchGetJson("%s/radio/txok" % (self.address)).keys())
            listAvailable.extend(self._launchGetJson("%s/radio/filter?mode=rx" % (self.address)).keys())
            listAvailable.extend(self._launchGetJson("%s/radio/filter?mode=tx" % (self.address)).keys())
        return listAvailable

    @property
    def allMeasure(self):
        if self.simulate:
            return {}
        else:
            allMeasuresList = self._launchGetJson("%s/measures" % (self.address))['measures']
            allValueList = []
            for measure in allMeasuresList:
                allValueList.append(self._launchGetJson("%s/measures/%s" % (self.address, measure))[measure])
            allMeasuresDict = dict(zip(allMeasuresList, allValueList))
            if self.tapHw == "TAPMV4.0":
                allMeasuresDict.update(self._launchGetJson("%s/radio/txok" % (self.address)))
                allMeasuresDict.update(self._launchGetJson("%s/radio/filter?mode=rx" % (self.address)))
                allMeasuresDict.update(self._launchGetJson("%s/radio/filter?mode=tx" % (self.address)))
            return allMeasuresDict

    @property
    def freqTx(self):
        return self._launchGetJson("%s/radio/freq/tx" % self.address)["tx"]

    @freqTx.setter
    def freqTx(self, value):
        self.logger.info("Change tx to %s" % str(value), ch = self.channel)
        self._launchPostJson("%s/radio/freq/tx" % self.address, {"tx":value})

    @property
    def freqRx(self):
        return self._launchGetJson("%s/radio/freq/rx" % self.address)["rx"]

    @freqRx.setter
    def freqRx(self, value):
        self.logger.info("Change rx to %s" % str(value), ch = self.channel)
        self._launchPostJson("%s/radio/freq/rx" % self.address, {"rx":value})

    @property
    def filterTx(self):
        return 0 #TODO

    @filterTx.setter
    def filterTx(self, value):
        self.logger.info("Change tx to %s" % str(value), ch = self.channel)
        if self.tapHw == "TAPMV4.0":
            self._launchPostJson("%s/radio/filter?mode=tx&filter=%s" % (self.address, str(value)))

    @property
    def filterRx(self):
        return 0 #TODO

    @filterRx.setter
    def filterRx(self, value):
        self.logger.info("Change rx to %s" % str(value), ch = self.channel)
        if self.tapHw == "TAPMV4.0":
            self._launchPostJson("%s/radio/filter?mode=rx&filter=%s" % (self.address, str(value)))

    @property
    def mode(self):
        return self._launchGetJson("%s/radio/mode" % self.address)['mode'].upper()

    @mode.setter
    def mode(self, value):
        self.logger.info("Change mode to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/mode" % self.address, {'mode':value})

    @property
    def preamp0(self):
        if self.tapHw != "TAPMV4.0":
            return self._launchGetJson("%s/radio/preamp?id=0" % (self.address))['preamp']
        else:
            return "NA"

    @preamp0.setter
    def preamp0(self, value):
        if self.tapHw != "TAPMV4.0":
            self.logger.info("Change preamp0 to %s" % value, ch = self.channel )
            self._launchPostJson("%s/radio/preamp?id=0" % (self.address), {'preamp':value})

    @property
    def preamp1(self):
        if self.tapHw == "TAPMV4.0":
            return self.preamp1_var
        return self._launchGetJson("%s/radio/preamp?id=1" % (self.address))['preamp']


    @preamp1.setter
    def preamp1(self, value):
        self.logger.info("Change preamp1 to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/preamp?id=1" % (self.address), {'preamp':value})
        if self.tapHw == "TAPMV4.0":
		    self.preamp1_var = value

    @property
    def preamp2(self):
        if self.tapHw != "TAPMV4.0":
            return self._launchGetJson("%s/radio/preamp?id=2" % (self.address))['preamp']
        else:
            return "NA"

    @preamp2.setter
    def preamp2(self, value):
        if self.tapHw != "TAPMV4.0":
            self.logger.info("Change preamp2 to %s" % value, ch = self.channel )
            self._launchPostJson("%s/radio/preamp?id=2" % (self.address), {'preamp':value})

    def nxpRegister(self, group = 0, index = 0, value=None):
        if self.tapHw != "TAPMV4.0":
            return None
        if value is None:
            return self._launchGetJson("%s/radio/nxp?group=%s&command=%s" % (self.address, group, index))['value']
        else:
            self.logger.info("Set Register %s to %s" % (group, index), ch = self.channel)
            self._launchPostJson("%s/radio/nxp?group=%s&command=%s&value=%s" % (self.address, group, index, value))

    def playBBSine(self, freqBBHz = 20000, timeSec = 1, atten = 10, dB = 0):
        if not self.simulate:
            try:
                freqList = float(freqBBHz)
            except:
                freqList = [float(x) for x in freqBBHz]
            else:
                freqList = [freqBBHz]
            if self.tapHw == "TAPMV4.0":
                self._launchGetJson("%s/radio/txok" % (self.address))
                if atten < 8:
                    atten = 8
                fs = 280000
            else:
                fs = 192000
            t = np.arange(fs * float(timeSec))
            samplesI = [0] * len(t)
            samplesQ = [0] * len(t)
            for freq in freqList:
                samplesI += (np.cos(2 * np.pi * float(freq) / fs * t))
                samplesQ += (np.sin(2 * np.pi * float(freq) / fs * t))
            signalRow = np.empty((samplesI.size + samplesQ.size))
            signalRow[0::2] = samplesI
            signalRow[1::2] = samplesQ
            signalRow /= np.max(signalRow)
            signalRow *= np.power(10.0, dB/20.0)
            signalRowF16_LE = (signalRow * 32766).astype(np.int16)
            dither = np.random.random_integers(-1, 1, len(signalRowF16_LE))
            signalRowF16_LE += dither
            try:
                self._launchPostData("%s/signal/playRaw?attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())
            except:
                self._launchPost("%s/signal/stop" % self.address)
                self._launchPostData("%s/signal/playRaw?attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())
            time.sleep(0.2)

    def stopBBSine(self):
        if not self.simulate:
            self._launchPost("%s/signal/stop" % (self.address))
            time.sleep(0.01)

    def playBBNoise(self, bwBBHz = 20000, timeSec = 1, atten = 10):
        if not self.simulate:
            try:
                BWList = float(bwBBHz)
            except:
                BWList = [float(x) for x in bwBBHz]
            else:
                BWList = [bwBBHz]
            if self.tapHw == "TAPMV4.0":
                if atten < 8:
                    atten = 8
                timeSec = "7"
                fs = 280000
            else:
                fs = 192000
            t = np.arange(fs * float(timeSec))
            noise = np.random.randn(len(t))
            for bw in BWList:
                fa = float(bw)
            fBW = float(fa / fs)
            noiseWindow = np.kaiser(len(t), 5)
            noise /= np.max(noise)
            if fBW < 0.95 :
                # FILTRE BUTTER #
                # b, a = signal.butter(10, float(fa / fs))
                # noiseBw = signal.filtfilt(b, a, noise)
                # FILTRE FIR #
                # b = signal.firwin(128, float(fa / fs), window='nuttall')
                # noiseBw = signal.convolve(noise,b)
                # FILTRE IIR #
                b, a = signal.iirdesign(fBW, (0.05 + fBW), 1, 120, analog=False, ftype='cheby2', output='ba')
                noiseBW = signal.filtfilt(b, a, noise) * noiseWindow
            else :
                noiseBW = noise * noiseWindow
            signalRow = np.empty((2 * noiseBW.size))
            signalRow[0::2] = noiseBW
            signalRow[1::2] = noiseBW
            signalRowF16_LE = (signalRow * 32766).astype(np.int16)
            try:
                self._launchPostData("%s/signal/playRaw?count=1&attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())
            except:
                self._launchPost("%s/signal/stop" % self.address)
                self._launchPostData("%s/signal/playRaw?count=1&attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())
            time.sleep(0.2)

    def stopBBNoise(self):
        if not self.simulate:
            self._launchPost("%s/signal/stop" % (self.address))
            time.sleep(0.01)

    def irrSin(self, freqBBHz = 20000):
        if self.simulate:
            return {'dGain': 0.0, 'dPhase': 0.0, 'irr': 0.0, 'rssi': 0.0}
        else:
            maxRetry = 3
            nbOfRetry = 0
            status = False
            while status is False:
                try:
                    self.logger.debug("Get irrSin at freqBBHz = {0}".format(freqBBHz))
                    resp = self.session.get("%s/signal/record" % (self.address), auth=('factory', 'factory'), stream=True, timeout=3)
                    if resp.status_code not in [200, 204]:
                        if resp.status_code == 500:
                            raise AcbbsError("Errors To record signal Dump %s" % self.dumpErrors(),
                                              ch=self.channel, log=self.logger)
                        else:
                            raise AcbbsError("Errors To record signal", ch=self.channel, log=self.logger)
                    p = subprocess.Popen("%s/toolIQ -f %s --int-gain 0 --ext-gain 0" % (os.path.dirname(os.path.abspath(__file__)), freqBBHz), stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                    pout = p.stdout
                    acquire = True
                    try:
                        for chunk in resp.iter_content(chunk_size=1024):
                            if acquire :
                                try:
                                    p.stdin.write(chunk)
                                except:
                                    self.stopBBSine()
                                    acquire = False
                    except:
                        self.stopBBSine()
                        raise AcbbsError("No Chunk receive", ch=self.channel, log=self.logger)
                    result = pout.readlines()[2].split(" ")
                    irr = {'dGain': float(result[7]), 'dPhase': float(result[9]), 'irr': float(result[11]), 'rssi': float(result[17])}
                    freq = float(result[14])
                    if ((freq > (int(freqBBHz) + 2000)) or (freq < (int(freqBBHz) - 2000))):
                        raise AcbbsError("ToolIQ bad freqBBHz freq read: %s expected: %s" % (freq, int(freqBBHz)),
                                         ch=self.channel, log=self.logger)
                    else:
                        self.logger.debug("return = {0}".format(irr))
                        return irr
                except:
                    if nbOfRetry >= maxRetry:
                        self.logger.error("Bad BB frequency irrSin: 4 tries to receive the correct frequency", ch ="%s" % self.channel)
                        return {'dGain': "NA", 'dPhase': "NA", 'irr': "NA", 'rssi': "NA"}
                    else:
                        if nbOfRetry == maxRetry -1 :
                            time.sleep(5)
                            self.logger.debug("nbOfRetry rssiSin: %s" %nbOfRetry , ch ="%s" % self.channel)
                        nbOfRetry = nbOfRetry + 1
                else:
                    status = True

    def _dumpErrors(self):
        errors  = self.session.get("%s/radio/fwErrors" % (self.address), auth=('factory', 'factory')).json()['errors']
        if not errors:
            return None
        self._launchPost("%s/radio/clearFwErrors" % self.address)
        return errors
