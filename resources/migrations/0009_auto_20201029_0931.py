# Generated by Django 3.0.8 on 2020-10-29 09:31

from django.db import migrations, models
import gdstorage.storage
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20201025_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='syll_url',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='syllabus',
            field=models.FileField(blank='True', default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=resources.models.path_and_rename_syllabus),
        ),
    ]
