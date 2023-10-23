from django.db import models


class Dashboard(models.Model):
    name = models.CharField(max_length=300, default='Digital Nugder')
