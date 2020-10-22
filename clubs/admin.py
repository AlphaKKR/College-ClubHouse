from django.contrib import admin
from . import models

admin.site.register(models.ClubAccount)
admin.site.register(models.ClubEvent)
admin.site.register(models.ClubBigEvent)
admin.site.register(models.Recruitment)
admin.site.register(models.BigRecruitment)
