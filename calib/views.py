import json

from django.shortcuts import HttpResponse, render
from django.http import JsonResponse

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError

from .tasks import Calibration
from .tasks import NetworkEquipment
from .tasks import database
from .tasks import MatrixCal

from .tasks import OUTPUTS
from .tasks import INPUTS


# Create your views here.

def home(request):
    db = database()
    listcalib = db.get_available_collection()
    if "system.indexes" in listcalib:
        listcalib.pop(0)
    return render(request, "calib/home.html", {"portsIN": INPUTS, "channels": OUTPUTS, "history": listcalib})


def checkInstrument(request):
    equipement = NetworkEquipment(simu=True)
    result = equipement.check_all_instruments()
    if result == 0:
        return JsonResponse({'msg': result})
    else:
        return JsonResponse({'msg': result})


# obtenir les configurartions de la calibration
def start_calib(request):
    if request.is_ajax():
        cmd = dict(request.GET)
        freq = json.loads(cmd["freq"][0])
        pwr = int(cmd["pwr"][0])
        calib = Calibration(pwr=pwr, tab_freq=freq, simu=True)
        calib.calibrate()
    return JsonResponse({'response': 'Switch calibrate'})

def getLossPath(request):
    matrix = MatrixCal()
    if request.is_ajax():
        portIN = dict(request.GET)['portIN'][0]
        portOUT = dict(request.GET)['portOUT'][0]
        date = dict(request.GET)['date'][0]
        data = matrix.getlossPath(portIN, portOUT, date)
        print(data)
        Xvalue = []  ### fréquence
        Yvalue = []  ### perte (dB)
        for key, value in data.items():
             Xvalue.append(int(key))
             Yvalue.append(value)
    return JsonResponse({"freq": Xvalue, "loss": Yvalue})

