from django.db import models
 
# Create your models here.

class Appnames(models.Model):
    print('model called')
    Appid=models.IntegerField()
    AppnNames=models.CharField(max_length=200)
   
    
