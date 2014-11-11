# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orderdetail_order_presentation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='price',
            field=models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
