# Generated by Django 2.1.2 on 2018-12-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0004_podcast_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='video_id',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]