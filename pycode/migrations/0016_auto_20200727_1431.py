# Generated by Django 3.0.8 on 2020-07-27 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0015_auto_20200727_1428'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='profile',
            new_name='user_profile',
        ),
    ]
