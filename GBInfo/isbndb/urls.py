
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'isbndb.views',
    url(r'^$', 'results', name='results'),
    )
