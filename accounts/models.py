from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, timetable=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('Use must have an username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            timetable=timetable,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    
class UserAccount(AbstractBaseUser):
    email           = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username        = models.CharField(verbose_name='username', max_length=30, unique=True)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)

    first_name      = models.CharField(default='', max_length=30)
    last_name       = models.CharField(default='', max_length=30)
    timetable       = models.TextField(default='', max_length=10000, null=True)
    club_verification = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserAccountManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

