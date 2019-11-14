from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        request.POST['email'] = request.POST['username']
        form = RegisterForm(request.POST)
