from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from models import Inbox
from core.views import JsonView
from forms import InboxCreateForm, ForwardRuleFormSet, UserCreateForm


class InboxList(JsonView):
    def prepare_context(self, request, *args, **kwargs):
        """ Prepare there your ansver. Must returns dict """
        return {'inboxes': list(request.user.inboxes.values('title', 'slug', 'users'))}


@login_required
def inbox_create(request):
    form = InboxCreateForm(request.POST or None, owner=request.user)
    if request.method == "POST":
        if form.is_valid():
            inbox = form.save()
            inbox.users.add(request.user)
            return redirect('home')
    context = {
        'inbox_form': form,
    }
    return render(request, 'core/home.html', context)


@login_required
def inbox_mails_list(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    context = {
        "inbox": inbox,
        "user_form": UserCreateForm(),
        "forward_formset": ForwardRuleFormSet(instance=inbox, prefix='forward_rule'),
    }
    return render(request, 'inbox/list.html', context)


@login_required
def inbox_forward_rule_create(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    formset = ForwardRuleFormSet(request.POST or None, instance=inbox,
        prefix='forward_rule')
    if formset.is_valid():
        formset.save()
        return redirect('inbox-mails-list', inbox.slug)
    context = {
        "inbox": inbox,
        "user_form": UserCreateForm(),
        "forward_formset": formset,
    }
    return render(request, 'inbox/list.html', context)


@login_required
def inbox_team_add(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    user_form = UserCreateForm(request.POST or None, inbox=inbox)
    if request.method == "POST" and user_form.is_valid():
        member = user_form.save()
        inbox.users.add(member)
        return redirect('inbox-mails-list', inbox.slug)
    context = {
        "inbox": inbox,
        "user_form": user_form,
    }
    forward_formset = ForwardRuleFormSet(instance=inbox, prefix='forward_rule')
    context.update({"forward_formset": forward_formset, })
    return render(request, 'inbox/list.html', context)
