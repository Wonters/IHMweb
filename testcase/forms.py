#!/usr/bin/python3 
# coding=UTF-8
import os

from django.forms import ModelForm

# sources
# models
from .models import Testcasemodel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# form to get manual set values
class testcaseForm(ModelForm):
    class Meta:
        model = Testcasemodel
        fields = '__all__'  # ['simulation', 'channel','configFile','name','climChamber']

# on peux rajouter des fonctions d'affichages et de traitements
