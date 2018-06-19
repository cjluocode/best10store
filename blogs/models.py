from django.db import models

# Create your models here.
class Blog(models.Model):

    title   = models.CharField(max_length=500)
    content = models.TextField(max_length=10000)
    image   = models.CharField(max_length=100)


    def __str__(self):

        return self.title
