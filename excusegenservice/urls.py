from django.conf.urls import patterns, include, url
from excusegenservice.excusegenservice.views import locationResolver

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^locationResolver/', locationResolver),
)
