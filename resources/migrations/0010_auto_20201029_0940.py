# Generated by Django 3.0.8 on 2020-10-29 09:40

from django.db import migrations, models
import gdstorage.storage
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0009_auto_20201029_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='syllabus',
            field=models.FileField(default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=resources.models.path_and_rename_syllabus),
        ),
    ]
