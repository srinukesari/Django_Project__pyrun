# Generated by Django 3.0.8 on 2020-07-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0020_auto_20200727_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='education',
            field=models.CharField(default='Not Mentioned', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='skill',
            field=models.CharField(default='C', max_length=50, null=True),
        ),
    ]
