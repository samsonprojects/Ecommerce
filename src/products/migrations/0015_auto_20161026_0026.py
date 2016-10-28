# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import products.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0014_myproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('height', models.CharField(null=True, max_length=20, blank=True)),
                ('width', models.CharField(null=True, max_length=20, blank=True)),
                ('media', models.ImageField(null=True, width_field='width', height_field='height', blank=True, upload_to=products.models.download_media_location)),
                ('product', models.ForeignKey(to='products.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='myproducts',
            options={'verbose_name': 'My Product', 'verbose_name_plural': 'My Products'},
        ),
    ]
