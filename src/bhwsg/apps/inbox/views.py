import itertools
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from models import Inbox
from core.views import JsonView
from forms import InboxCreateForm, ForwardRuleFormSet, UserCreateForm
from inbox.decorators import check_inbox, mail_required
from inbox.models import Mail


class InboxList(JsonView):
    def prepare_context(self, request, *args, **kwargs):
        response = list()
        for inbox in Inbox.objects.get_user_inboxes(request.user):
            response.append({
                'title': inbox.title,
                'label': inbox.label,
                'slug': inbox.slug,
                'url': reverse('inbox-list', args=(inbox.slug,)),
                'count': inbox.mails.count(),
                'unread': inbox.unreaded_mails,
                'users': list(inbox.users.values_list('id', flat=True)),
            })
        response.insert(0, {
            'title': "All",
            'label': None,
            'slug': '/',
            'url': reverse('home'),
            'count': reduce(lambda x, y: x + y, [inbox['count'] for inbox in response]),
            'unread': reduce(lambda x, y: x + y, [inbox['unread'] for inbox in response]),
            'users': list(set(itertools.chain.from_iterable([inbox['users'] for inbox in response]))),
        })
        return {'inboxes': response}


class InboxMailList(JsonView):
    @check_inbox
    def prepare_context(self, request, *args, **kwargs):
        if request.inbox:
            mails = Mail.objects.get_inbox_mails(request.inbox)
        else:
            # Get mails from all inboxes
            mails = Mail.objects.get_user_mails(request.user)
            
        from_date = request.GET.get('from_date')
        if from_date:
            mails = mails.filter(date__gt=from_date)

        count = request.GET.get('count', 50)
        if count and count != 'all':
            mails = mails[:count]

        prepare_mail_data = lambda mail: {
            'subject': mail.subject,
            'from_email': mail.from_email_pretty,
            'to_email': mail.to_email,
            'date': mail.date.strftime('%Y-%m-%d %H:%M:%S'),
            'readed': mail.is_readed(request.user),
            'few_lines': mail.few_lines,
            'url': reverse('mail-json', args=(mail.id,))
        }

        return {'mails': map(prepare_mail_data, mails)}


class MailView(JsonView):
    @mail_required
    def prepare_context(self, request, *args, **kwargs):
        params = request.GET
        mail = request.mail

        data = {'result': True}
        if 'mark_readed' in params:
            mail.readers.add(request.user)
        elif 'delete' in params:
            mail.delete()
        else:
            # return mail
            if 'raw' in params:
                data['raw'] = mail.raw
            else:
                data.update({
                    'plain': mail.has_text() and mail.get_text() or None,
                    'html': mail.has_html() and mail.get_html() or None,
                    'from_email': mail.from_email_pretty,
                    'to_email': mail.to_email,
                    'bcc': mail.bcc,
                    'cc': mail.cc,
                    'subject': mail.subject,
                    'date': mail.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'attachments': [attchmnt.file.url for attchmnt in mail.attachments.all()]
                })

        return data


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


@login_required
def inbox_delete(request, slug):
    inbox = get_object_or_404(Inbox, slug=slug)
    if request.user == inbox.owner:
        inbox.delete()
    return redirect('home')
