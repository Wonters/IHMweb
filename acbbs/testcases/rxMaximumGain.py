# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

class rxMaximumGain(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)
