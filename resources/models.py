from django.db import models
import os

def path_and_rename_cat1(instance, filename):
    upload_to = 'papers/cat1'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_{}.{}'.format(instance.pk, 'cat1', ext)

    return os.path.join(upload_to, filename)

def path_and_rename_cat2(instance, filename):
    upload_to = 'papers/cat2'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_{}.{}'.format(instance.pk, 'cat2', ext)

    return os.path.join(upload_to, filename)

def path_and_rename_fat(instance, filename):
    upload_to = 'papers/fat'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_{}.{}'.format(instance.pk, 'fat', ext)

    return os.path.join(upload_to, filename)

class CAT1(models.Model):
    course_code     = models.CharField(null=False, default='', max_length=200, primary_key=True)
    subject         = models.CharField(null=True, default='', max_length=200)
    cat_1           = models.FileField(upload_to=path_and_rename_cat1, default='', null=True)
    date            = models.DateTimeField(auto_now_add=True, null=True, editable=True)

    def delete(self, using=None, keep_parents=False):
        self.cat_1.storage.delete(self.cat_1.name)
        super().delete()
    
    def __str__(self):
        return self.course_code

    class Meta:
        verbose_name = 'CAT 1 Paper'
        verbose_name_plural = 'CAT 1 papers'

class CAT2(models.Model):
    course_code     = models.CharField(null=False, default='', max_length=200, primary_key=True)
    subject         = models.CharField(null=True, default='', max_length=200)
    cat_2           = models.FileField(upload_to=path_and_rename_cat2, default='', null=True)
    date            = models.DateTimeField(auto_now_add=True, null=True, editable=True)

    def delete(self, using=None, keep_parents=False):
        self.cat_2.storage.delete(self.cat_2.name)
        super().delete()

    def __str__(self):
        return self.course_code

    class Meta:
        verbose_name = 'CAT 2 Paper'
        verbose_name_plural = 'CAT 2 papers'

class FAT(models.Model):
    course_code     = models.CharField(null=False, default='', max_length=200, primary_key=True)
    subject         = models.CharField(null=True, default='', max_length=200)
    fat_paper       = models.FileField(upload_to=path_and_rename_fat, default='', null=True)
    date            = models.DateTimeField(auto_now_add=True, null=True, editable=True)

    def delete(self, using=None, keep_parents=False):
        self.fat_paper.storage.delete(self.fat_paper.name)
        super().delete()

    def __str__(self):
        return self.course_code

    class Meta:
        verbose_name = 'FAT Paper'
        verbose_name_plural = 'FAT Papers'