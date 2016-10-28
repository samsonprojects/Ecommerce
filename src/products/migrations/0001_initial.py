# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.DecimalField(default=9.99, max_digits=100, decimal_places=2)),
                ('sale_price', models.DecimalField(blank=True, null=True, default=6.99, decimal_places=2, max_digits=100)),
            ],
        ),
    ]
