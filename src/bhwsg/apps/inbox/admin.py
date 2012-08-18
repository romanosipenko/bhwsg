from django.contrib import admin
from inbox.models import Inbox, InboxSettings, ForwardRule, DeleteRule, Mail

admin.site.register(Inbox)
admin.site.register(InboxSettings)
admin.site.register(ForwardRule)
admin.site.register(DeleteRule)
admin.site.register(Mail)
