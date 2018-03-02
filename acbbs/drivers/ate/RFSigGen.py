# coding=UTF-8
from acbbs.tools.log import *

class RFSigGen(object):
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

    def status(self, status = None):
        """


        @param  status :
        @return  :
        @author
        """
        pass

    def power(self, value = None):
        """


        @param  value :
        @return  :
        @author
        """
        pass

    def freq(self, value = None):
        """


        @param  value :
        @return  :
        @author
        """
        pass

    def __readWrite(self, cmd = None, value = None):
        """


        @param  cmd :
        @param  value :
        @return  :
        @author
        """
        pass

    def __wait(self):
        """


        @return  :
        @author
        """
        pass
