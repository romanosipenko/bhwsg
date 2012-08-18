import logging
from celery.decorators import task
from annoying.functions import get_object_or_None

from inbox.models import Mail, Inbox

logger = logging.getLogger('core.tasks')

@task
def handle_mail(mail_dict):
    """
        Save mail to Inbox model. Check and apply handlig rules for email.
    """
    inbox = get_object_or_None(Inbox, slug=mail_dict.pop('inbox'))
    
    if inbox:
        mail = Mail.objects.create(inbox=inbox, **mail_dict)
        for rule in inbox.get_rules(mail):
            try:
                rule.apply(mail)
            except Exception, e:
                logger.error('Rule execution failed: %s' % e)
    