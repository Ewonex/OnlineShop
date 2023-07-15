from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    data = {

    }
    return render(request, 'main/index.html', data)

def authorization(request):
    data = {

    }
    return render(request, 'main/authorization.html', data)

def registration(request):
    data = {

    }
    return render(request, 'main/registration.html', data)