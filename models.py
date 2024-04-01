from django.db import models

class UserSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    history = models.JSONField(null=True)
# Create your models here.
