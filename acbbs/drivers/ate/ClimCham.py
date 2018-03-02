# coding=UTF-8
from acbbs.tools.log import *

class ClimCham(object):
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

    def enable(self):
        """


        @return  :
        @author
        """
        pass

    @property
    def tempConsigne(self):
        return None

    @property
    def tempReal(self):
        return None

    @property
    def humidityConsigne(self):
        return None

    @property
    def humidityReal(self):
        return None
