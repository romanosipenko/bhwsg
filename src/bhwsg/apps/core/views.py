from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from inbox.forms import InboxCreateForm


def home(request):
    inbox_form = InboxCreateForm()
    context = {
        'inbox_form': inbox_form
    }
    return render(request, 'core/home.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/auth.html')


def logout_user(request):
    logout(request)
    return redirect('home')
