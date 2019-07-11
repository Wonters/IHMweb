#! /usr/bin/python3 
# coding=UTF-8

from django.forms import ModelForm

# sources
# models
from .models import ConfFile


class UploadFileForm(ModelForm):
    class Meta:
        model = ConfFile
        fields = '__all__'
