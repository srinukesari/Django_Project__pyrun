# Generated by Django 3.0.8 on 2020-07-20 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0005_auto_20200720_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem_table',
            name='problem_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pycode.questions'),
        ),
    ]
