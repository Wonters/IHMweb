# coding=UTF-8
from acbbs.tools.log import *

class DCPwr(object):
    def __init__(self, simulate = False):
        """


        @param bool simulate :
        @return  :
        @author
        """
        pass

    def getErrors(self):
        return []

    @property
    def reference(self):
        return ""

    @property
    def version(self):
        return ""

    @property
    def status(self):
        return ""

    @property
    def voltageConsigne(self):
        return None

    @property
    def voltageReal(self):
        return None

    @property
    def currentConsigne(self):
        return None

    @property
    def currentReal(self):
        return None

    def __wait(self, channel = 1):
        """


        @param int channel :
        @return  :
        @author
        """
        pass

    def __channelSel(self, channel = 1):
        """


        @param int channel :
        @return  :
        @author
        """
        pass

    def __readWrite(self, channel = 1, cmd = None, value = None):
        """


        @param int channel :
        @param  cmd :
        @param  value :
        @return  :
        @author
        """
        pass
