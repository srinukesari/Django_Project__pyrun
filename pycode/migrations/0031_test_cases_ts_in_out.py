# Generated by Django 3.0.8 on 2020-07-29 04:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0030_auto_20200728_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_cases',
            name='ts_in_out',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]
