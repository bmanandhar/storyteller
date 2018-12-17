from django.db import models
 
# Create your models here.
class Story(models.Model):
    user = models.CharField(max_length=200)
    body = models.TextField()
    date = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


