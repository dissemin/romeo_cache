# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

import lxml.etree as ET
from io import BytesIO

MAX_DATA_LENGTH = 512

class Record(models.Model):
    data = models.CharField(max_length=MAX_DATA_LENGTH, unique=True)
    fetched = models.DateTimeField(auto_now=True)
    body = models.TextField()

def delete_invalid_records():
    batch_size = 100
    idx = 0
    rec_count = Record.objects.count()
    while idx < rec_count:
        print idx
        for r in Record.objects.all().order_by('id')[idx:(idx+batch_size)]:
            try:
                parser = ET.XMLParser(encoding='utf-8')
                ET.parse(BytesIO(r.body.encode('utf-8')), parser)
            except ET.ParseError as e:
                print "Pruning record "+r.data
                r.delete()
                idx -= 1
        idx += batch_size

