# Generated by Django 3.0.8 on 2020-07-19 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0003_challenges'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenges',
            old_name='challenge_hackathon',
            new_name='challenge_type',
        ),
    ]