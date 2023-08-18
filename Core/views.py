from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from Core.forms import SignUpForm


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('welcome')
    else:
        form = SignUpForm()
    return render(request, 'Core/registration.html', {'form': form})


def welcome(request):
    return render(request, 'Core/welcome.html')
