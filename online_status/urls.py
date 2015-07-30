from django.conf.urls import patterns, url
from online_status.views import test, example, users

urlpatterns = patterns(
    '',
    url(r'^test/$', test, name='online_users_test'),
    url(r'^example/$', example, name='online_users_example'),
    url(r'^$', users, name='online_users'),
)
