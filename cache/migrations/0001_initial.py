# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.CharField(unique=True, max_length=512)),
                ('fetched', models.DateTimeField(auto_now=True)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
