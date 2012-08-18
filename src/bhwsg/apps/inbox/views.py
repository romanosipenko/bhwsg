from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from models import Inbox
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


@login_required
def inbox_mails_list(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    return render(request, 'inbox/list.html', {'inbox': inbox, })
