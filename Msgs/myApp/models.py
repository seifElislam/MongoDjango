from django.db import models

class Message(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=100)
