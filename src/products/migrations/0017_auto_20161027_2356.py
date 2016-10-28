# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20161027_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(upload_to=products.models.download_media_location, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/Army1/Desktop/djangoClients/Ecommerce/my_env/static_cdn/protected'), blank=True),
        ),
    ]
