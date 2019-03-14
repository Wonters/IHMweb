#! /usr/bin/python3 
# coding=UTF-8

from django import forms


# sources
# models


# a travailler
# pour utiliser un formulaire et obtenir la valeur du select il faut faire une liste de choices !!!!!  
class selectConfigDbForm(forms.Form):
    configName = forms.TypedChoiceField(
        widget=forms.Select)  # (coerce="string",error_messages={'required': 'Please choose a configuration'})
