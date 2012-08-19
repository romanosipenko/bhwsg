from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from forms import LoginForm
from inbox.forms import InboxCreateForm


def home(request):
    inbox_form = InboxCreateForm()
    context = {
        'inbox_form': inbox_form
    }
    return render(request, 'core/home.html', context)


def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.authenticate()
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/auth.html', {"form": form})


def logout_user(request):
    logout(request)
    return redirect('home')
