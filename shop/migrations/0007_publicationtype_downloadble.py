# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_order_payment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationtype',
            name='downloadble',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
