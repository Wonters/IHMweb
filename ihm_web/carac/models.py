#!/usr/bin/python3 
# coding=UTF-8
from __future__ import unicode_literals

import os

from django.db import models

import jsonfield

# sources
# form

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Save settings to start the characterization
class Testcasemodel(models.Model):
    testcase_simulation = models.BooleanField()
    testcase_channels = models.IntegerField()
    testcase_type = models.TextField(null=True)
    testcase_nameCarac = models.TextField(null=True)
    testcase_climChamber = models.BooleanField()

    def __str__(self):
        return self.testcase_nameCarac

class Campagnmodel(models.Model):
    campagn_channels = models.CharField(max_length=100)
    campagn_type = models.CharField(max_length=200)
    campagn_name = models.CharField(max_length=200)
    campagn_climChamber = models.CharField(max_length=50)
    campagn_date = models.CharField(max_length=200)
    campagn_clim_total = models.IntegerField()
    campagm_clim_current = models.IntegerField()
    campagn_tc2play = models.CharField(max_length=400)
    campagn_templist = models.CharField(max_length=200)

class Progressbar(models.Model):
    current = models.IntegerField()
    total = models.IntegerField()
    tc_current = models.IntegerField()
    tc_total = models.IntegerField()
    tc = models.CharField(max_length=100)
    responseTask = models.CharField(max_length=100)
    temperature = models.IntegerField()
    state = models.IntegerField()


class ConfFile(models.Model):
    file = models.FileField()


