import logging
from celery.decorators import task
from annoying.functions import get_object_or_None

from inbox.models import Mail, Inbox
from core.parsers import MailParser

logger = logging.getLogger('core.tasks')

@task
def handle_mail(mail_dict):
    """
        Save mail to Inbox model. Check and apply handlig rules for email.
    """
    inbox = get_object_or_None(Inbox, slug=mail_dict.pop('inbox'))
    
    if inbox:
        parser = MailParser(mail_dict['raw'])
        
        mail = Mail.objects.create(
            inbox=inbox,
            content_types=parser.get_content_types(),
            **mail_dict
        )
        for rule in inbox.get_rules():
            try:
                rule.apply(mail)
            except Exception, e:
                logger.error('Rule execution failed: %s' % e)
    