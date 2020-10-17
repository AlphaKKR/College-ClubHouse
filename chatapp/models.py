from django.db import models
from accounts.models import UserAccount


class Room(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    name = models.TextField(max_length=200, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    ipaddress = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    name = models.TextField(max_length=100, null=True)
    messages = models.TextField(max_length=10000, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    ipaddress = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.messages