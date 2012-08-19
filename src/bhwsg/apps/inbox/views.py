from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from models import Inbox
from core.views import JsonView
from forms import InboxCreateForm, ForwardRuleFormSet, UserCreateForm
from inbox.decorators import inbox_required
from inbox.models import Mail


class InboxList(JsonView):
    def prepare_context(self, request, *args, **kwargs):
        response = list()
        for inbox in Inbox.objects.get_user_inboxes(request.user):
            response.append({
                'title': inbox.title,
                'label': inbox.label,
                'slug': inbox.slug,
                'mails_count': inbox.mails.count(),
                'mails_unreaded_count': inbox.unreaded_mails,
                'users': list(inbox.users.values_list('id', flat=True)),
            })
        return {'inboxes': response}


class InboxMailList(JsonView):
    @inbox_required
    def prepare_context(self, request, *args, **kwargs):
        mails = Mail.objects.get_inbox_mails(request.inbox, request.user)
        from_date = request.GET.get('from_date')

        if from_date:
            mails = mails.filter(date__gt=from_date)

        count = request.GET.get('count', 50)
        if count and count != 'all':
            mails = mails[:count]

        prepare_mail_data = lambda mail: {
            'subject': mail.subject,
            'from_email': mail.from_email,
            'to_email': mail.to_email,
            'date': mail.date.strftime('%Y-%m-%d %H:%M:%S'),
            'readed': mail.is_readed(request.user),
            'few_lines': mail.few_lines
        }

        return {'mails': map(prepare_mail_data, mails)}


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


@login_required
def inbox_team_remove_me(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    if request.user in inbox.users.all():
        inbox.users.remove(request.user)
    if not inbox.users.exists():
        inbox.delete()
    return redirect('home')
