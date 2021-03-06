# Generated by Django 3.0.8 on 2020-07-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycode', '0013_test_cases'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_username', models.CharField(max_length=30)),
                ('skills', models.CharField(default=' ', max_length=200)),
                ('education', models.CharField(default=' ', max_length=50)),
                ('ques_solved', models.IntegerField(default=0)),
                ('profile_pic', models.ImageField(upload_to='profile_pics')),
            ],
        ),
    ]
