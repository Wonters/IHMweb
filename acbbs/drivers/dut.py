# coding=UTF-8
from acbbs.tools.log import *
from acbbs.tools.configurationFile import *

import requests
import os

folder = os.path.dirname(os.path.abspath(__file__))
#Set log class in connectionpool Class with the CustomLog class
requests.packages.urllib3.connectionpool.log.__class__ = log
#Rename log name
requests.packages.urllib3.connectionpool.log.name = "connectionPool"

TIMEOUT = 2

class dut(object):
    class _simulate(object):
        class post(object):
            def __init__(self, uri, json=None, timeout=None):
                pass

            @property
            def status_code(self):
                return 200

        class get(object):
            def __init__(self, uri, stream=None, timeout=None):
                pass

            def iter_content(chunk_size=None):
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

    def __init__(self , chan=None, simulate = False):
        '''
        Constructor
        '''

        #init logs
        self.logger = get_logger(self.__class__.__name__)

        #simulation state
        self.simulate = simulate

        #get configuration
        self.conf = configurationFile(file = self.__class__.__name__)
        self.dutConf = self.conf.getConfiguration()

        if chan is None:
            raise AcbbsError("Channel mandatory", log=self.logger)

        self.channel = chan
        self.ip = self.dutConf["ip"] % self.channel

        #case of simulate
        if simulate :
            self.logger.info("Init dut in Simulate", ch=self.channel)
            self.session = self._simulate()

        else :
            self.logger.info("Init dut")
            self.session = requests.Session()

        self.address = "http://%s/factory" % self.ip
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
            self.logger.error("dut error, aborting...", ch = chan)

    def _launchCmd(self, uri, get = True, payloadJson = None, payloadData = None, stream = False, callback = None):
        if get:
            resp = self.session.get(uri, stream=stream, timeout=TIMEOUT)
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
            if resp.status_code not in [200, 204]:
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
                resp = self.session.post(uri, json=payloadJson, timeout=TIMEOUT)
            elif payloadData:
                resp = self.session.post(uri, data=payloadData, headers={'Content-Type': 'application/octet-stream'}, timeout=TIMEOUT)
            else:
                resp = self.session.post(uri, timeout=TIMEOUT)
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
        return self._launchGetJson("%s/measures" % (self.address))['measures']

    @property
    def allMeasure(self):
        if self.simulate:
            return {}
        else:
            allMeasuresList = self.allMeasureAvailable
            allValueList = []
            for measure in allMeasuresList:
                allValueList.append(self._launchGetJson("%s/measures/%s" % (self.address, measure))[measure])
            return dict(zip(allMeasuresList, allValueList))

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
    def mode(self):
        return self._launchGetJson("%s/radio/mode" % self.address)['mode'].upper()

    @mode.setter
    def mode(self, value):
        self.logger.info("Change mode to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/mode" % self.address, {'mode':value})

    @property
    def preamp0(self):
        return self._launchGetJson("%s/radio/preamp?id=0" % (self.address))['preamp']

    @preamp0.setter
    def preamp0(self, value):
        self.logger.info("Change preamp0 to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/preamp?id=0" % (self.address), {'preamp':value})

    @property
    def preamp1(self):
        return self._launchGetJson("%s/radio/preamp?id=1" % (self.address))['preamp']

    @preamp1.setter
    def preamp1(self, value):
        self.logger.info("Change preamp1 to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/preamp?id=1" % (self.address), {'preamp':value})

    @property
    def preamp2(self):
        return self._launchGetJson("%s/radio/preamp?id=2" % (self.address))['preamp']

    @preamp2.setter
    def preamp2(self, value):
        self.logger.info("Change preamp2 to %s" % value, ch = self.channel )
        self._launchPostJson("%s/radio/preamp?id=2" % (self.address), {'preamp':value})

    def nxpRegister(self, group = 0, index = 0, value=None):
        if value is None:
            return self._launchGetJson("%s/radio/nxp?group=%s&command=%s" % (self.address, group, index))['value']
        else:
            self.logger.info("Set Register %s to %s" % (group, index), ch = self.channel)
            self._launchPostJson("%s/radio/nxp?group=%s&command=%s&value=%s" % (self.address, group, index, value))

    def playBBSine(self, freqBBHz = 20000, timeSec = 1, atten = 10):
        try:
            freqList = float(freqBBHz)
        except:
            freqList = [float(x) for x in freqBBHz]
        else:
            freqList = [freqBBHz]
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
        signalRowF16_LE = (signalRow * 32766).astype(np.int16)
        dither = np.random.random_integers(-1, 1, len(signalRowF16_LE))
        signalRowF16_LE += dither
        try:
            self._launchPostData("%s/signal/playRaw?count=0&attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())
        except:
            self._launchPost("%s/signal/stop" % self.address)
            self._launchPostData("%s/signal/playRaw?attenLevel=%s" % (self.address, atten), signalRowF16_LE.tostring())

    def stopBBSine(self):
        self._launchPost("%s/signal/stop" % (self.address))
        time.sleep(0.01)

    def playBBNoise(self, bwBBHz = 20000, timeSec = 1, atten = 10):
        try:
            BWList = float(bwBBHz)
        except:
            BWList = [float(x) for x in bwBBHz]
        else:
            BWList = [bwBBHz]
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
            b, a = sig.iirdesign(fBW, (0.05 + fBW), 1, 120, analog=False, ftype='cheby2', output='ba')
            noiseBW = sig.filtfilt(b, a, noise) * noiseWindow
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

    def stopBBNoise(self):
        self._launchPost("%s/signal/stop" % (self.address))
        time.sleep(0.01)

    def rssiSin(self, freqBBHz = 20000):
        if self.simulate:
            return "xxxx"

    def irrSin(self, freqBBHz = 20000):
        if self.simulate:
            return "xxxx"

    def _dumpErrors(self):
        errors = []
        while True:
            resp = self.session.get("%s/radio/nxp?group=0&command=2" % (self.address)).json()['value']
            if resp is 0:
                break
            errors.append(hex(int(resp)))
        if not errors:
            return None
        return errors
