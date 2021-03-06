# Generated by Django 3.0.8 on 2020-11-01 06:31

import clubs.models
from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0008_auto_20201025_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bigrecruitment',
            name='poster',
            field=models.ImageField(blank=True, default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=clubs.models.path_and_rename_recs),
        ),
        migrations.AlterField(
            model_name='clubaccount',
            name='club_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='clubaccount',
            name='club_logo',
            field=models.ImageField(blank=True, default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=clubs.models.path_and_rename_logos),
        ),
        migrations.AlterField(
            model_name='clubevent',
            name='event_poster',
            field=models.ImageField(blank=True, default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=clubs.models.path_and_rename_events),
        ),
        migrations.AlterField(
            model_name='recruitment',
            name='recruit_poster',
            field=models.ImageField(blank=True, default='', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=clubs.models.path_and_rename_recs),
        ),
    ]
