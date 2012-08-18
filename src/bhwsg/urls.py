from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.core.views import home, login_user, logout_user

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', home, name="home"),
    url(r'^login/$', login_user, name="auth_login"),
    url(r'^logout/$', logout_user, name="auth_logout"),
)
