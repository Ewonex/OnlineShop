from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('authorization', views.authorization, name='authorization_page'),
    path('registration', views.registration, name='registration_page'),
]
