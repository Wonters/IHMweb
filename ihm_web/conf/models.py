# Create your models here.
# !/usr/bin/python3
# coding=UTF-8
from __future__ import unicode_literals

import os

from django.db import models

# sources
# form

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ConfFile(models.Model):
    file = models.FileField()
