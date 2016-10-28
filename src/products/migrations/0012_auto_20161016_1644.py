# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='media',
            field=models.FileField(upload_to=products.models.download_media_location, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='managers',
            field=models.ManyToManyField(related_name='managers_product', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
