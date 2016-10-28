# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0010_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='managers',
            field=models.ManyToManyField(related_name='managers_product', to=settings.AUTH_USER_MODEL),
        ),
    ]
