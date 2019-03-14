#!/usr/bin/python3 
# coding=UTF-8
from __future__ import unicode_literals

import os

from django.db import models

# sources
# form

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Save settings to start the characterization
class Testcasemodel(models.Model):
    testcase_simulation = models.BooleanField()
    testcase_channel = models.IntegerField()
    testcase_type = models.TextField(null=True)
    testcase_nameCarac = models.TextField(null=True)
    testcase_climChamber = models.BooleanField()

    def __str__(self):
        return self.testcase_nameCarac


class Progressbar(models.Model):
    progress_value = models.IntegerField()
