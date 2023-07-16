from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import User
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView
def index(request):
    data = {

    }
    return render(request, 'main/index.html', data)

def authorization(request):
    data = {

    }
    return render(request, 'main/authorization.html', data)

def registration(request):
    error = []
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()#Сохранение в таблице
            return redirect('/authorization')
        else:
            for field, errors in form.errors.items():
                field_label = form.fields[field].label
                error.append(f"{field_label}: {', '.join(errors)}")
            error = ", ".join(error)
    form = RegistrationForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/registration.html', data)
