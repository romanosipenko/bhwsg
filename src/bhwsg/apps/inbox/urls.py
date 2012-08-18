from django.conf.urls import patterns, url

from views import inbox_create

urlpatterns = patterns('',
    url(r'create/', inbox_create, name="inbox-create"),
)
