import json

from django.shortcuts import HttpResponse, render
from django.http import JsonResponse

from .tasks import SwitchCalibration
from .tasks import WiresCalibration
from .tasks import NetworkEquipment

from .tasks import LIST_PATH
from .tasks import CHANNELS
from .tasks import INPUTS


# Create your views here.

def home(request):
    return render(request, "calib/home.html", {"portsIN": INPUTS, "channels": CHANNELS})


def checkInstrument(request):
    equipement = NetworkEquipment(simu=True)
    result = equipement.check_all_instruments()
    if result == 0:
        return JsonResponse({'msg': result})
    else:
        return JsonResponse({'msg': result})


# obtenir les configurartions de la calibration
def start_calibSwitch(request):
    if request.is_ajax():
        print(request.GET)
        calib = SwitchCalibration(pwr=2, tab_freq=[1, 3, 4, 5, 6], simu=True)
        calib.calibrate()
    return JsonResponse({'response': 'Switch calibrate'})


def start_calibWires(request):
    if request.is_ajax():
        data = request.GET['parameters']
        data = json.loads(data)
        print(data)
        calib = WiresCalibration(tab_freq=data['freq'].split(','), pwr=data['pwr'], channels=data['channels'],
                                 simu=True, inputs=data['ports'])
        calib.calibrate()
    return JsonResponse({'response': 'Wires calibrate'})
