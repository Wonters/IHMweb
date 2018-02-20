# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

import time
from os.path import basename, splitext

class rxGainLNAs(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)
        self.db = dataBase(name = "{0}_{1}".format(splitext(basename(__file__))[0], time.strftime("%Y_%m_%d_%H:%M:%S")))

    def run(self):
        pass

    def test(self):
        pass
