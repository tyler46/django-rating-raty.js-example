from django.conf.urls import *

urlpatterns = patterns('circus.demos.views',
    url(r'^$', 'list_shows', name='demos_list_shows'),
    url(r'^(?P<slug>[A-Za-z0-9-]+)/$', 'view_show',
        name='demos_view_show'),
    url(r'^(?P<slug>[A-Za-z0-9-]+)/rate/$', 'rate_show',
        name='demos_rate_show')
)
