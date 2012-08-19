from django.conf.urls import patterns, url

from views import inbox_create, inbox_mails_list, inbox_forward_rule_create

urlpatterns = patterns('',
    url(r'create/', inbox_create, name="inbox-create"),
    url(r'rules/forward/(?P<slug>[-\w]+)/', inbox_forward_rule_create,
        name="inbox-forward-rule-create"),
    url(r'(?P<slug>[-\w]+)/', inbox_mails_list, name="inbox-mails-list"),
)
