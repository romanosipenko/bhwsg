import os
import logging
import  fnmatch
import re
from annoying.functions import get_object_or_None
from functools import partial
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify, striptags, truncatewords_html
from django.core.files.base import ContentFile
from django.core.mail import send_mail

from core.fields import JSONField
from core.utils import memoize_method
from core.parsers import MailParser, TEXT_PLAIN_CONTENT_TYPE,\
    TEXT_HTML_CONTENT_TYPE

logger = logging.getLogger('inbox')


class InboxManager(models.Manager):
    def get_user_inboxes(self, user, q_filter=None, q_exclude=None):
        queryset = self.get_query_set().filter(users=user)

        if q_filter:
            queryset = queryset.filter(**q_filter)
        if q_exclude:
            queryset = queryset.exclude(**q_exclude)

        unreaded_letters = list(
            Mail.objects.filter(inbox__in=queryset)\
            .exclude(readers=user)\
            .values_list('inbox', flat=True)
        )

        for inbox in queryset:
            inbox.unreaded_mails = len(filter(lambda x: x == inbox.id, unreaded_letters))
            yield inbox

    def get_inbox(self, user, **kwargs):
        queryset = self.get_query_set().filter(users=user).prefetch_related('users')
        return get_object_or_None(queryset, **kwargs)


class Inbox(models.Model):
    title = models.CharField(max_length=50)
    label = models.CharField(max_length=10, blank=True, null=True)
    slug = models.SlugField("SMTP login/Permalink", max_length=255, unique=True,
        blank=True, null=True)
    password = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='inboxes')
    owner = models.ForeignKey(User, related_name='owned_inboxes', blank=True, null=True)

    objects = InboxManager()

    class Meta:
        ordering = ('slug',)
        unique_together = (('title', 'label'),)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'inbox-mails-list', (self.slug,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_title)
        super(Inbox, self).save(*args, **kwargs)

    @property
    def full_title(self):
        return u"%s %s" % (self.title, self.label or "")

    @property
    def login(self):
        return self.slug

    def get_mails(self, user):
        """ Get inbox mails for current user """

        mails = self.mails.filter().order_by('-date')
        mails = mails.prefetch_related('readers', '')

    def get_settings(self):
        """ Get inbox settings """
        return self.settings.all()


class InboxSettings(models.Model):
    inbox = models.ForeignKey(Inbox, related_name="settings")

    mask = models.CharField(max_length=255, blank=True, null=True)

    FORWARD = 'forwardrule'
    DELETE = 'deleterule'
    RULES = [
        FORWARD,
        DELETE,
    ]

    def get_correct_rule(self):
        for rule in self.RULES:
            if hasattr(self, rule):
                return getattr(self, rule)
        else:
            return None

    def apply(self, mail):
        """Apply settings to certain mail"""
        raise NotImplemented

    def detail(self):
        raise NotImplemented


class ForwardRule(InboxSettings):
    email_to = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return '%s, %s' % (self.inbox, self.detail)

    @property
    def detail(self):
        return u'Forward rule: to - %s, mask - %s' % (self.email_to or 'N/A', self.mask)

    def apply(self, mail):
        if self.mask:
            for mail in self.email_to:
                regex = fnmatch.translate(self.mask)
                reobj = re.compile(regex)
                if reobj.match(self.email_to):
                    forward = True
            else:
                forward = False
            if forward:
                send_mail(mail.subject, mail.message, mail.from_email, [self.email_to])


class DeleteRule(InboxSettings):
    NOT_READED = 0
    READED = 1
    READED_BY_ALL = 2
    READED_CHOICES = (
        (NOT_READED, "All"),
        (READED, "Readed"),
        (READED_BY_ALL, "Readed by all"),
    )
    period = models.PositiveSmallIntegerField(blank=True, null=True)
    readed = models.PositiveSmallIntegerField(blank=True, null=True,
        choices=READED_CHOICES)

    @property
    def detail(self):
        return u'Delete rule: to - %s, mask - %s' % (self.email_to, self.mask)

    def apply(self):
        pass


class MailManager(models.Manager):
    def new_mail(self, inbox, raw_data):
        """
            Add new mail
        """
        parser = Mail.parser(raw_data['raw'])

        raw_data.update({
            'from_email': parser.get_from(),
            'to_email': parser.get_to(),
            'content_types': parser.get_content_types(),
            'content_type': parser.get_content_type(),
            'bcc': parser.get_bcc(),
            'cc': parser.get_cc(),
            'subject': parser.get_subject()
        })

        mail = self.create(
            inbox=inbox,
            **raw_data
        )

        attachment = partial(MailAttachment, mail=mail)

        # Save attacments
        MailAttachment.objects.bulk_create(
            [attachment(file=ContentFile(ac, n)) for n, ac in parser.get_attachments()]
        )
        # Apply rules
        for settings in inbox.get_settings():
            try:
                settings.get_correct_rule().apply(mail)
            except Exception, e:
                logger.error('Rule execution failed: %s' % e)

    def get_inbox_mails(self, inbox, user):
        queryset = self.get_query_set().filter(inbox=inbox)
        queryset = queryset.prefetch_related('readers').order_by('-date')
        return queryset

    def get_mail(self, user, **kwargs):
        queryset = self.get_query_set().filter(inbox__users=user)
        queryset = queryset.prefetch_related('readers')

        return get_object_or_None(queryset, **kwargs)


class Mail(models.Model):
    parser = MailParser

    inbox = models.ForeignKey(Inbox, related_name="mails")
    readers = models.ManyToManyField(User, related_name="mails")
    peer = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255,
        help_text="The email address, and optionally the name of the author(s)")
    to_email = JSONField(
        help_text="The email address(es), and optionally name(s) of the message's recipient(s)."
    )
    bcc = JSONField(blank=True, null=True,
        help_text="Blind Carbon Copy")
    cc = JSONField(blank=True, null=True,
        help_text="Carbon copy")
    raw = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True,
        help_text="A brief summary of the topic of the message.")
    uuid = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True,
        help_text="The local time and date when the message was written.")

    # All content types of letter
    content_types = JSONField(blank=True, null=True)

    objects = MailManager()

    def __unicode__(self):
        return u'Mail for %s' % self.inbox

    @memoize_method
    def get_parser(self):
        """ Returns object that has access to different parts of mail """
        return self.parser(self.raw)

    @property
    def content_type(self):
        return self.content_types and self.content_types[0] or None

    def has_html(self):
        return TEXT_HTML_CONTENT_TYPE in self.content_types

    def has_text(self):
        return TEXT_PLAIN_CONTENT_TYPE in self.content_types

    def has_attachments(self):
        pass

    def get_html(self):
        return self.get_parser().get_html()

    def get_text(self):
        return self.get_parser().get_text()

    def get_attachments(self):
        return self.attachments.objects.all()

    def is_readed(self, user):
        return True if self.readers.filter(id=user.id).count() else False

    @property
    def few_lines(self):
        return striptags(truncatewords_html(self.get_text(), 20))


def get_attachment_upload_path(instance, name):
    name = name.encode('utf-8')
    return os.path.join('attachments', str(instance.mail.id), name)


class MailAttachment(models.Model):
    mail = models.ForeignKey(Mail, related_name='attachments')
    file = models.FileField(upload_to=get_attachment_upload_path)
