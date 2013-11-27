from django.conf.urls import patterns, include, url
from excusegenservice.views import locationResolver, generateExcuses

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^locationResolver/', locationResolver),
    url(r'^generateExcuses/', generateExcuses),
)
