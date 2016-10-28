# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20161016_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(upload_to=products.models.download_media_location, blank=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/Army1/Desktop/djangoClients/Ecommerce/my_env/static_cdn/protected'), null=True),
        ),
    ]
