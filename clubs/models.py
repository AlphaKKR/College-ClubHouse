from django.db import models
from django.db.models.functions import Cast
import os

def path_and_rename_logos(instance, filename):
    upload_to = 'clubs/logos'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)

        return os.path.join(upload_to, filename)

def path_and_rename_events(instance, filename):
    upload_to = 'clubs/events'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)

        return os.path.join(upload_to, filename)

def path_and_rename_recs(instance, filename):
    upload_to = 'clubs/recruitments'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    
        return os.path.join(upload_to, filename)



class ClubAccount(models.Model):
    club_name       = models.CharField(null=False, default='', max_length=1000, primary_key=True)
    club_website    = models.URLField(null=True)
    ig_url          = models.URLField(null=True)
    club_email      = models.EmailField(null=True, unique=True)
    club_logo       = models.ImageField(upload_to=path_and_rename_logos, default='', null=True)

    def delete(self, using=None, keep_parents=False):
        self.club_logo.storage.delete(self.club_logo.name)
        super().delete()


    def __str__(self):
        return self.club_name

class ClubEvent(models.Model):
    club_name       = models.ForeignKey(ClubAccount, on_delete=models.CASCADE, null=True)
    event_name      = models.CharField(max_length=100 ,default='', null=False, primary_key=True)
    event_desc      = models.TextField(default='', max_length=1000, null=True)
    event_poster    = models.ImageField(upload_to=path_and_rename_events, default='', null=True)
    event_url       = models.URLField(default='', null=True)
    
    def __str__(self):
        return (str(self.event_name) + " -- " + str(self.club_name))

    def delete(self, using=None, keep_parents=False):
        self.event_poster.storage.delete(self.event_poster.name)
        super().delete()


class ClubBigEvent(models.Model):
    club_name       = models.ForeignKey(ClubAccount, on_delete=models.CASCADE, null=True)
    event_name      = models.CharField(max_length=100 ,default='', null=False, primary_key=True)
    event_desc      = models.TextField(default='', max_length=1000, null=True)
    image           = models.ImageField(upload_to=path_and_rename_events, default='', null=True)
    event_url       = models.URLField(default='', null=True)

    def __str__(self):
        return (str(self.event_name) + " -- " + str(self.club_name))

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

class Recruitment(models.Model):
    club_name       = models.OneToOneField(ClubAccount, on_delete=models.CASCADE, null=False, primary_key=True)
    rec_date_time   = models.DateTimeField(null=True)
    rec_desc        = models.TextField(max_length=1000, default='', null=True)
    recruit_poster  = models.ImageField(upload_to=path_and_rename_recs, default='', null=True)

    def __str__(self):
        return str(self.club_name)

    def delete(self, using=None, keep_parents=False):
        self.recruit_poster.storage.delete(self.recruit_poster.name)
        super().delete()


class BigRecruitment(models.Model):
    club_name       = models.OneToOneField(ClubAccount, on_delete=models.CASCADE, null=False, primary_key=True)
    rec_date_time   = models.DateTimeField(null=True)
    rec_desc        = models.TextField(max_length=1000, default='', null=True)
    poster          = models.ImageField(upload_to=path_and_rename_recs, default='', null=True)

    def __str__(self):
        return str(self.club_name)

    def delete(self, using=None, keep_parents=False):
        self.poster.storage.delete(self.poster.name)
        super().delete()

