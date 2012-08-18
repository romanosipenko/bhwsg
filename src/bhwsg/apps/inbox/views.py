from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms import InboxCreateForm


@login_required
def inbox_create(request):
    form = InboxCreateForm(request.POST or None, owner=request.user)
    if request.method == "POST":
        if form.is_valid():
            inbox = form.save()
            inbox.users.add(request.user)
            return redirect('home')
    else:
        context = {
            'inbox_form': form,
        }
        return render(request, 'core/home.html', context)
