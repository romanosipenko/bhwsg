from django.db import models
from django.contrib.auth.models import User


class Inbox(models.Model):
    login = models.CharField(max_length=255, unique=True,
        help_text="SMTP login/Permalink")
    password = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='inboxes')

    class Meta:
        ordering = ('login',)

    def __unicode__(self):
        return self.title


class Mail(models.Model):
    inbox = models.ForeignKey(Inbox)

    def __unicode__(self):
        return u'Mail for %s' % self.inbox
