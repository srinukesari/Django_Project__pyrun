# Generated by Django 3.0.8 on 2020-07-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=100)),
                ('question_type', models.CharField(choices=[('Easy', 'easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('advance', 'Advance')], default='easy', max_length=10)),
                ('question_score', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='check',
        ),
    ]
