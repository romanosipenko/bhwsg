from django.http import Http404
from core.views import PermisionDenited
from inbox.models import Inbox

def inbox_required(func):
    def _check_inbox(self, request, *args, **kwargs):
        if not kwargs.get('slug'):
            raise Http404
        if not request.user.is_authenticated():
            raise PermisionDenited
        
        inbox = Inbox.objects.get_inbox(user=request.user, slug=kwargs['slug'])
        if not inbox:
            raise PermisionDenited
        
        request.inbox = inbox
        
        return func(self, request, *args, **kwargs) 
    
    return _check_inbox