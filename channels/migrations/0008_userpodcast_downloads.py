# Generated by Django 2.1.2 on 2019-02-02 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0007_userpodcast_duration_listened'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpodcast',
            name='downloads',
            field=models.IntegerField(default=0),
        ),
    ]
