from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from allauth.account.views import PasswordResetView

from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def send_reset_password_email(sender, instance, created, **kwargs):

    if created:

        # First create a post request to pass to the view
        request = HttpRequest()
        request.method = 'POST'

        # add the absolute url to be be included in email
        if settings.DEBUG:
            request.META['HTTP_HOST'] = '127.0.0.1:8000'
        else:
            request.META['HTTP_HOST'] = 'www.mysite.com'

        # pass the post form data
        request.POST = {
            'email': instance.email,
            'csrfmiddlewaretoken': get_token(HttpRequest())
        }
        PasswordResetView.as_view()(request)  # email will be sent!

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

