#!/usr/bin/python2.7
# coding=UTF-8

import os

class app(object):
    def __init__(self):
        self.path = os.path.realpath(__file__).split(self.__class__.__name__)[0]
        self.tcFolder = []
        for file in os.listdir("{0}/testcases".format(self.path)):
            if file.endswith(".py"):
                self.tcFolder.append(os.path.join("acbbs/testcases", file))

    def getTestcases(self):
        tclist = []
        for tc in self.tcFolder:
            tclist.append(tc.split('/')[2].split('.')[0])

        for f2d in ["__init__", "skeletonTc", "baseTestCase"]:
            tclist.remove(f2d)
        tclist.sort()
        return tclist

    def openTestcase(self, tc):
        # import testcases
        cmd = "from acbbs.testcases.{0} import *".format(tc)
        exec cmd

        cmd = "threadTc = {0}()".format(tc)
        exec cmd
        return threadTc

if __name__ == '__main__':
    a = app()
