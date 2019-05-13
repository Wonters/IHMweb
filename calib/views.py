import json

from django.shortcuts import HttpResponse, render
from django.http import JsonResponse


from .tasks import SwitchCalibration
from .tasks import WiresCalibration
from .tasks import NetworkEquipment


# Create your views here.

def home(request):
    return render(request, "calib/home.html")


def checkInstrument(request):
    equipement = NetworkEquipment()
    result = equipement.check_all_instruments()
    if result == 0:
        return JsonResponse({'msg': "done"})
    else:
        return JsonResponse({'msg': "error"})


# obtenir les configurartions de la calibration

def get_calibParameters(request):
    # ajax request to get freiquency range from the front
    if request.is_ajax():
        parameters = dict(request.GET[0])
    return parameters


def start_calibSwitch(request):
    parameters = get_calibParameters(request)
    # Calib = Calibration(parent=None, freq=parameters['calibFreq'],channels=parameters['calibChannels'],
    #                     simu= parameters['simulate'],pwr=parameters['calibPwr'],conf=parameters['calibConf'])
    #calib = SwitchCalibration(parent='None', freq=3, pwr=2, channels=[1, 2, 3], conf=None, simu=True)
    print()

def start_calibWires(request):

    calib = WiresCalibration(tab_freq=[3, 4, 5], pwr=2, channels=[1, 2, 3], simu=True, inputs=["J2", "J4", "J18"])
    calib.calibrate()

    return HttpResponse('OK')

