# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20141108_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='price',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='thumbnail',
            field=models.ImageField(default=b'', upload_to=b'thumbnails'),
            preserve_default=True,
        ),
    ]
