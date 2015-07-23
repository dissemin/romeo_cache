# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

MAX_DATA_LENGTH = 512

class Record(models.Model):
    data = models.CharField(max_length=MAX_DATA_LENGTH, unique=True)
    fetched = models.DateTimeField(auto_now=True)
    body = models.TextField()

