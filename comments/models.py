from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Comment(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)    
    story   = models.ForeignKey('story.Story',on_delete=models.CASCADE)
    body    = models.TextField()
    date    = models.IntegerField()

    def __str__(self):
        return self.date

class Like(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)    
    story   = models.ForeignKey('story.Story',on_delete=models.CASCADE)
    types   = models.CharField(max_length=8)
    date    = models.IntegerField()

    def __str__(self):
        return self.types

