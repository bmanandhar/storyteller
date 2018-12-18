from django.db import models
import datetime

# Create your models here.

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    story = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user
