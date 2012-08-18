from django.conf.urls import patterns, url

from views import inbox_create, inbox_mails_list

urlpatterns = patterns('',
    url(r'create/', inbox_create, name="inbox-create"),
    url(r'(?P<slug>[-\w]+)/', inbox_mails_list, name="inbox-mails-list"),
)
