from django.shortcuts import render


# Create your views here.


# Return the home page of home application
def home(request):
    return render(request, 'home/home.html')
