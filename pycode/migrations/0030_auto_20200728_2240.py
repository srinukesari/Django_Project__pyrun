# Generated by Django 3.0.8 on 2020-07-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0029_auto_20200727_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='mobile',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='whatsapp',
            field=models.BigIntegerField(default=0),
        ),
    ]
