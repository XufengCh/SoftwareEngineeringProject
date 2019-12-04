from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            username = request.POST['username']
            email = request.POST['username']
            nickname = request.POST['nickname']
            password = request.POST['password1']
            User.objects.create_user(username=username, email=email, nickname=nickname, password=password).save()
            # return to the index
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form})
