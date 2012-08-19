from django.http import Http404
from core.views import PermisionDenited
from inbox.models import Inbox, Mail


def check_inbox(func):
    """
        Decorator that checks access to inbox if slug is given. Add inbox instance to request.
    """

    def _check_inbox(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermisionDenited

        if kwargs.get('slug'):
            inbox = Inbox.objects.get_inbox(user=request.user, slug=kwargs['slug'])
            if not inbox:
                raise Http404
        else:
            inbox = None

        request.inbox = inbox

        return func(self, request, *args, **kwargs)

    return _check_inbox


def mail_required(func):
    """
        Decorator, that checks access to mail and adds mail instance to request.
    """

    def _check_mail(self, request, *args, **kwargs):
        if not kwargs.get('mail_id'):
            raise Http404
        if not request.user.is_authenticated():
            raise PermisionDenited
        mail = Mail.objects.get_mail(request.user, id=kwargs['mail_id'])
        if not mail:
            raise Http404

        request.mail = mail

        return func(self, request, *args, **kwargs)

    return _check_mail
