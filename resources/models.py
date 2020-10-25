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

def path_and_rename_cat1(instance, filename):
    upload_to = 'cat1/'
    ext = filename.split('.')[-1]
    filename = '{} {} {}.{}'.format(instance.course, instance.date, 'cat1', ext)

    return os.path.join(upload_to, filename)

def path_and_rename_cat2(instance, filename):
    upload_to = 'cat2/'
    ext = filename.split('.')[-1]
    filename = '{} {} {}.{}'.format(instance.course, instance.id, 'cat2', ext)

    return os.path.join(upload_to, filename)

def path_and_rename_fat(instance, filename):
    upload_to = 'fat/'
    ext = filename.split('.')[-1]
    filename = '{} {} {}.{}'.format(instance.course, instance.id, 'fat', ext)

    return os.path.join(upload_to, filename)

class Subject(models.Model):
    course_code     = models.CharField(null=False, default='', max_length=200, primary_key=True)
    subject         = models.CharField(null=True, default='', max_length=200)
    date            = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.course_code


class CAT1files(models.Model):
    course          = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    cat_1           = models.FileField(upload_to=path_and_rename_cat1, default='', null=True, storage=gd_storage)
    cat_1_url       = models.URLField(default='', null=True, blank=True)
    date            = models.DateTimeField(auto_now_add=True, null=True)
   
    def __str__(self):
        return str(self.course) + ' Sub id: ' + str(self.id)
    
    class Meta:
        verbose_name = 'CAT 1 File'
        verbose_name_plural = 'CAT 1 Files'

@receiver(post_delete, sender=CAT1files)
def submission_delete_cat1(sender, instance, **kwargs):
    instance.cat_1.delete(False)

class CAT2files(models.Model):
    course          = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    cat_2           = models.FileField(upload_to=path_and_rename_cat2, default='', null=True, storage=gd_storage)
    date            = models.DateTimeField(auto_now_add=True, null=True)
    cat_2_url       = models.URLField(default='', null=True, blank=True)

    def __str__(self):
        return str(self.course) + ' Sub id: ' + str(self.id)

    class Meta:
        verbose_name = 'CAT 2 File'
        verbose_name_plural = 'CAT 2 Files'

@receiver(post_delete, sender=CAT2files)
def submission_delete_cat2(sender, instance, **kwargs):
    instance.cat_2.delete(False)

class FATfiles(models.Model):
    course          = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)    
    fat_paper       = models.FileField(upload_to=path_and_rename_fat, default='', null=True, storage=gd_storage)
    date            = models.DateTimeField(auto_now_add=True, null=True)
    fat_url         = models.URLField(default='', null=True, blank=True)



    def __str__(self):
        return str(self.course) + ' Sub id: ' + str(self.id)

    class Meta:
        verbose_name = 'FAT File'
        verbose_name_plural = 'FAT Files'

@receiver(post_delete, sender=FATfiles)
def submission_delete_fat(sender, instance, **kwargs):
    instance.fat_paper.delete(False)