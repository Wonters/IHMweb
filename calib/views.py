from django.shortcuts import HttpResponse, render

from .tasks import Calibration


# Create your views here.

def home(request):
    return render(request, "calib/home.html")


def test_ping(request):
    Calib = Calibration(parent='None', freq=3, pwr=2, channels=[1, 2, 3], conf=None, simu=None)
    Calib.rxCalibration()
    return HttpResponse("Please")


# obtenir les configurartions de la calibration

def get_calibParameters(request):
    # ajax request to get freiquency range from the front
    if request.is_ajax():
        parameters = dict(request.GET[0])
    return parameters


def start_calib(request):
    parameters = get_calibParameters(request)
    # Calib = Calibration(parent=None, freq=parameters['calibFreq'],channels=parameters['calibChannels'],
    #                     simu= parameters['simulate'],pwr=parameters['calibPwr'],conf=parameters['calibConf'])
    Calib = Calibration(parent='None', freq=3, pwr=2, channels=[1, 2, 3], conf=None, simu=None)

    print('bonjour, la calibration commence !')
