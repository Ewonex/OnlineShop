from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .models import User
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView
def index(request):
    data = {

    }
    return render(request, 'main/index.html', data)

def registration(request):
    error = []
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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

def authorization(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            error = 'Неверное имя пользователя или пароль'
            return render(request, 'main/authorization.html', {'error': error})
    else:
        return render(request, 'main/authorization.html')

def logout_user(request):
    logout(request)
    return redirect('main_page')

def catalogShow(request):
    data = {

    }
    return render(request, 'main/catalog.html', data)