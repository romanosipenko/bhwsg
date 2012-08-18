from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify, striptags, truncatewords_html


class Inbox(models.Model):
    title = models.CharField(max_length=50)
    label = models.CharField(max_length=10, blank=True, null=True)
    slug = models.CharField("SMTP login/Permalink", max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='inboxes')

    class Meta:
        ordering = ('slug',)
        unique_together = ('title', 'label')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_title)
        super(Inbox, self).save(*args, **kwargs)

    @property
    def full_title(self):
        return u"%s %s" % (self.title, self.label)

    @property
    def login(self):
        return self.slug

    def get_rules(self):
        """ Get inbox rules """

        rules = list(ForwardRule.objects.filter(inbox=self))
        return rules


class InboxSettings(models.Model):
    inbox = models.ForeignKey(Inbox, related_name="settings")

    def get_rules(self, mail):
        return []

    def apply(self, mail):
        """Apply settings to certain mail"""
        raise NotImplemented()


class Rule(InboxSettings):
    mask = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def get_correct_rule(self):
        return self.kind


class ForwardRule(Rule):
    kind = 'forwardrule'
    email_to = models.CharField(max_length=255, blank=True, null=True)

    def apply(self, mail):
        pass


class DeleteRule(Rule):
    kind = 'deleterule'

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

    def apply(self):
        pass


class Mail(models.Model):
    inbox = models.ForeignKey(Inbox, related_name="mails")
    readers = models.ManyToManyField(User, related_name="mails")
    peer = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255,
        help_text="The email address, and optionally the name of the author(s)")
    to_email = models.TextField(
        help_text="The email address(es), and optionally name(s) of the message's recipient(s).")
    bcc = models.TextField(blank=True, null=True,
        help_text="Blind Carbon Copy")
    cc = models.TextField(blank=True, null=True,
        help_text="Carbon copy")
    content_type = models.TextField(blank=True, null=True,
        help_text="Information about how the message is to be displayed, usually a MIME type.")
    raw = models.TextField(blank=True, null=True)
    subject = models.TextField(max_length=255, blank=True, null=True,
        help_text="A brief summary of the topic of the message.")
    message = models.TextField(blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True,
        help_text="The local time and date when the message was written.")

    def __unicode__(self):
        return u'Mail for %s' % self.inbox

    def readed(self):
        return self.readers.all().exists()

    def readed_by_all(self):
        return self.readers.all() == self.inbox.users.all()

    @property
    def few_lines(self):
        return striptags(truncatewords_html(self.message, 20))
