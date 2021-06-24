# Generated by Django 3.0.8 on 2020-07-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0010_auto_20200723_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='explanation',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='questions',
            name='constraints',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='questions',
            name='problem',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='questions',
            name='sample_input',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='questions',
            name='sample_output',
            field=models.TextField(default=None),
        ),
    ]
