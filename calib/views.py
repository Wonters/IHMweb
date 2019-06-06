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


class CalView():
    def __init__(self):
        self.db = database()
        self.calib = Calibration(simu=True)

    def home(self, request):
        listcalib = self.db.get_available_collection()
        if "system.indexes" in listcalib:
            listcalib.pop(0)
        return render(request, "calib/home.html", {"portsIN": INPUTS, "channels": OUTPUTS, "history": listcalib})


    def checkInstrument(self,request):
        result = self.calib.equipement.check_all_instruments()
        if result == 0:
            return JsonResponse({'msg': result})
        else:
            return JsonResponse({'msg': result})


    # obtenir les configurartions de la calibration
    def start_calib(self, request):
        if request.is_ajax():
            cmd = dict(request.GET)
            freq = json.loads(cmd["freq"][0])
            pwr = int(cmd["pwr"][0])
            self.calib.calibrate(tab_freq=freq, pwr=pwr)
        return JsonResponse({'response': 'Switch calibrate'})

    def getLossPath(self, request):
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

    def ProgressBackend(self, request):
        if request.is_ajax():
            self.progress = self.calib.iteration
            self.total = self.calib.totalProgress
            self.message = self.calib.message
            print(self.message)
        return JsonResponse({"current": self.progress, "total": self.total, "message": self.message})

    def response(self, request):
        print(dict(request.GET)["response"])
        self.calib.response = dict(request.GET)["response"]
        return JsonResponse({"":""})


