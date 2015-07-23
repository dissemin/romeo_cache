# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.utils.http import urlencode
from django.utils import timezone

import requests
import requests.exceptions

from datetime import timedelta, datetime

from cache.models import *

allowed_parameters = set(['pub','qtype','showfunder','id','jtitle','zetocpub','romeopub','issn','all','colour'])

record_life = timedelta(days=3*30)

base_url = 'http://sherpa.ac.uk/romeo/api29.php'

def perform_query(request):
    if request.method != 'GET':
        return HttpResponseForbidden('Invalid method', content_type='text/plain')
    args = request.GET.copy()
    if not 'ak' in args:
        return HttpResponseForbidden('An API key is required', content_type='text/plain')
    else:
        del args['ak']
    encoded = urlencode(args)
    if not all(map(lambda x: x in allowed_parameters, args.keys())) or len(encoded) > MAX_DATA_LENGTH:
        return HttpResponseForbidden('Invalid parameters', content_type='text/plain')
    
    r = None
    try:
        r = Record.objects.get(data=encoded)
        if timezone.now() - r.fetched < record_life:
            return HttpResponse(r.body, content_type='text/xml')
    except Record.DoesNotExist:
        pass

    resp = urlopen_retry(base_url, data=request.GET)
    if r is None:
        r = Record(data=encoded,body=resp)
    else:
        r.body = resp
    # TODO ensure we don't save some errors such as invalid api key
    if not '<outcome>invalidapikey</outcome>' in resp:
        r.save()
    return HttpResponse(resp, content_type='text/xml')

def urlopen_retry(url, **kwargs):# data, timeout, retries, delay, backoff):
    data = kwargs.get('data', None)
    timeout = kwargs.get('timeout', 10)
    retries = kwargs.get('retries', 4)
    delay = kwargs.get('delay', 5)
    backoff = kwargs.get('backoff', 2)
    headers = kwargs.get('headers', {})
    try:
        r = requests.get(url,
                params=data,
                timeout=timeout,
                headers=headers,
                allow_redirects=True)
        return r.text
    except requests.exceptions.Timeout as e:
        if retries <= 0:
            raise MetadataSourceException('Timeout: '+str(e))
    except requests.exceptions.ConnectionError as e:
        if retries <= 0:
            raise MetadataSourceException('Connection error: '+str(e))
    except requests.exceptions.RequestException as e:
        raise MetadataSourceException('Request error: '+str(e))

    print "Retrying in "+str(delay)+" seconds..."
    print "URL: "+url
    sleep(delay)
    return urlopen_retry(url,
            data=data,
            timeout=timeout,
            retries=retries-1,
            delay=delay*backoff,
            backoff=backoff)


