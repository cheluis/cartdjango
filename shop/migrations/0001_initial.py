# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(auto_now=True)),
                ('order_status', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'ACTIVE'), (b'P', b'PROCESSED'), (b'D', b'DOWNLOADED')])),
                ('order_address', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_quantity', models.IntegerField()),
                ('order', models.ForeignKey(to='shop.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'PaymentMethod',
                'verbose_name_plural': 'PaymentMethods',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date_published', models.DateField()),
                ('author', models.CharField(max_length=255)),
                ('pdf_file', models.FileField(null=True, upload_to=b'')),
                ('audio_file', models.FileField(null=True, upload_to=b'')),
                ('categories', models.ManyToManyField(to='shop.Category')),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'PublicationType',
                'verbose_name_plural': 'PublicationTypes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_types',
            field=models.ManyToManyField(to='shop.PublicationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_item',
            field=models.ForeignKey(to='shop.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='order_payment_method',
            field=models.ForeignKey(to='shop.PaymentMethod', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
