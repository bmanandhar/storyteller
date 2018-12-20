from django.db import models
from django.contrib.auth.models import User
import time

# Create your models here.

class Story(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)    
    body = models.TextField()
    date =  models.IntegerField()
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

