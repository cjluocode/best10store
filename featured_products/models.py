from django.db import models

# Create your models here.

class FeatureProduct(models.Model):
    title     = models.CharField(max_length=500)
    link      = models.CharField(max_length=500)
    rating    = models.FloatField()
    rating_count = models.IntegerField()
    image        = models.CharField(max_length=500)
    price        = models.CharField(max_length=500)
    hotscore    = models.IntegerField()
    query_word  = models.CharField(max_length=500, null=True, blank=True)
    goodreads_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title