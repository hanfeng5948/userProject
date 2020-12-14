from django.urls import path
from .views import *

urlpatterns = [
    path('login.html', loginView, name='login'),
    path('register.html', registerView, name='register'),
    path('setps.html', setpsView, name='setps'),
    path('logout.html', logoutView, name='logout'),
    path('', findpsView, name='findps')
]