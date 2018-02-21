# coding=UTF-8

from acbbs.testcases.baseTestCase import *
from acbbs.drivers.dut import *
from acbbs.drivers.ate.SpecAn import *
from acbbs.drivers.ate.RFSigGen import *

from os.path import basename, splitext

class rxGainLNAs(baseTestCase):
    def __init__(self):
        baseTestCase.__init__(self)
        self.db = dataBase(collection = splitext(basename(__file__))[0])
