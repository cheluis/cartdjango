# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_publicationtype_downloadble'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicationtype',
            old_name='downloadble',
            new_name='downloadable',
        ),
    ]
