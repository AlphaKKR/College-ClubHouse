from django.db import models
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

gd_storage = GoogleDriveStorage()
# permission =  GoogleDriveFilePermission(
#    GoogleDrivePermissionRole.READER,
#    GoogleDrivePermissionType.USER,
#    "127.0.0.1:8000"
# )

def path_and_rename_logos(instance, filename):
    upload_to = 'logos/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)

        return os.path.join(upload_to, filename)

def path_and_rename_events(instance, filename):
    upload_to = 'events/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)

        return os.path.join(upload_to, filename)

def path_and_rename_recs(instance, filename):
    upload_to = 'recruitments/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    
        return os.path.join(upload_to, filename)


class ClubAccount(models.Model):
    club_name       = models.CharField(null=False, default='', max_length=1000, primary_key=True)
    club_website    = models.URLField(null=True)
    ig_url          = models.URLField(null=True)
    club_email      = models.EmailField(null=True, unique=True)
    logo_url        = models.URLField(default='', null=True, blank=True)
    club_logo       = models.ImageField(upload_to=path_and_rename_logos, default='', null=True, storage=gd_storage)

    def __str__(self):
        return self.club_name


@receiver(post_delete, sender=ClubAccount)
def submission_delete_logo(sender, instance, **kwargs):
    instance.club_logo.delete(False)

class ClubEvent(models.Model):
    club_name       = models.ForeignKey(ClubAccount, on_delete=models.CASCADE, null=True)
    event_name      = models.CharField(max_length=100 ,default='', null=False, primary_key=True)
    event_desc      = models.TextField(default='', max_length=1000, null=True)
    event_poster    = models.ImageField(upload_to=path_and_rename_events, default='', null=True, storage=gd_storage)
    poster_url      = models.URLField(default='', null=True, blank=True)
    event_url       = models.URLField(default='', null=True)

    def __str__(self):
        return (str(self.event_name) + " -- " + str(self.club_name))


@receiver(post_delete, sender=ClubEvent)
def submission_delete_event(sender, instance, **kwargs):
    instance.event_poster.delete(False)
    

class ClubBigEvent(models.Model):
    club_name       = models.ForeignKey(ClubAccount, on_delete=models.CASCADE, null=True)
    event_name      = models.CharField(max_length=100 ,default='', null=False, primary_key=True)
    event_desc      = models.TextField(default='', max_length=1000, null=True)
    image           = models.ImageField(upload_to=path_and_rename_events, default='', null=True, storage=gd_storage)
    img_url         = models.URLField(default='', null=True, blank=True)
    event_url       = models.URLField(default='', null=True)

    def __str__(self):
        return (str(self.event_name) + " -- " + str(self.club_name))

@receiver(post_delete, sender=ClubBigEvent)
def submission_delete_bigev(sender, instance, **kwargs):
    instance.image.delete(False)

class Recruitment(models.Model):
    club_name       = models.OneToOneField(ClubAccount, on_delete=models.CASCADE, null=False, primary_key=True)
    rec_date_time   = models.DateTimeField(null=True)
    rec_desc        = models.TextField(max_length=1000, default='', null=True)
    recruit_poster  = models.ImageField(upload_to=path_and_rename_recs, default='', null=True, storage=gd_storage)
    poster_url      = models.URLField(default='', null=True, blank=True)

    def __str__(self):
        return str(self.club_name)

@receiver(post_delete, sender=Recruitment)
def submission_delete_recr(sender, instance, **kwargs):
    instance.recruit_poster.delete(False)

class BigRecruitment(models.Model):
    club_name       = models.OneToOneField(ClubAccount, on_delete=models.CASCADE, null=False, primary_key=True)
    rec_date_time   = models.DateTimeField(null=True)
    rec_desc        = models.TextField(max_length=1000, default='', null=True)
    poster          = models.ImageField(upload_to=path_and_rename_recs, default='', null=True, storage=gd_storage)
    poster_url      = models.URLField(default='', null=True, blank=True)

    def __str__(self):
        return str(self.club_name)


@receiver(post_delete, sender=BigRecruitment)
def submission_delete_bigrecr(sender, instance, **kwargs):
    instance.poster.delete(False)