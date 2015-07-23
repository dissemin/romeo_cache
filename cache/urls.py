# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cache.views import *

urlpatterns = patterns('',
        url(r'^romeo/api29.php$', perform_query, name='perform_query'),
)

