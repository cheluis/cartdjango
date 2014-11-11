# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20141110_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='order_presentation',
            field=models.ForeignKey(blank=True, to='shop.PublicationType', null=True),
            preserve_default=True,
        ),
    ]
