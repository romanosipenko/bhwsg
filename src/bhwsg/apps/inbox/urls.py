from django.conf.urls import patterns, url

from views import inbox_create, inbox_mails_list, inbox_forward_rule_create, \
    inbox_team_add, InboxList, InboxMailList, inbox_leave, inbox_delete, \
    inbox_settings

urlpatterns = patterns('',
    url(r'^settings/', inbox_settings, name="inbox-settings"),
    url(r'^create/', inbox_create, name="inbox-create"),
    url(r'^mail_list/$', InboxMailList.as_view(), name="inbox-mail-list"),
    url(r'^mail_list/(?P<slug>[-\w]+)/$', InboxMailList.as_view(), name="inbox-mail-list"),
    url(r'^list/$', InboxList.as_view(), name="inbox-list"),
    url(r'^delete/(?P<slug>[-\w]+)/$', inbox_delete, name="inbox-delete"),
    url(r'^rules/forward/(?P<slug>[-\w]+)/$', inbox_forward_rule_create,
        name="inbox-forward-rule-create"),
    url(r'^team/add/(?P<slug>[-\w]+)/$', inbox_team_add, name="inbox-team-add"),
    url(r'^team/leave/(?P<slug>[-\w]+)/$', inbox_leave, name="inbox-leave"),
    url(r'^(?P<slug>[-\w]+)/$', inbox_mails_list, name="inbox-mails-list"),
)
