from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from core.views import home, login_user, logout_user
from inbox.views import MailView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inbox/', include('inbox.urls')),
    url(r'^mail/(?P<mail_id>[\d]+)', MailView.as_view(), name="mail-json"),
    url(r'^$', home, name="home"),
    url(r'^login/$', login_user, name="auth_login"),
    url(r'^logout/$', logout_user, name="auth_logout"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
