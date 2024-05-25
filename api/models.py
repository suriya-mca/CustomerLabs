import uuid
import secrets
from django.db import models


class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    account_name = models.CharField(max_length=50)
    app_secret_token = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    website = models.CharField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = secrets.token_urlsafe(50)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.CharField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField()

    def __str__(self):
        return self.url