# Generated by Django 3.0.8 on 2020-07-29 04:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0031_test_cases_ts_in_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_cases',
            name='ts_in_out',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=2), blank=True, null=True, size=9),
        ),
    ]
