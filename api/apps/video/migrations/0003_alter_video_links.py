# Generated by Django 4.2 on 2023-04-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='links',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
