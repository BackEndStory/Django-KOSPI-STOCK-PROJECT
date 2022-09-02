from django.db import models

# Create your models here.


class Stockname_stocks(models.Model):
    stockname = models.CharField(max_length=50)
    stockcode = models.CharField(max_length=50)
    objects = models.Manager()



class Document(models.Model):
    title = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to="")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)
    objects = models.Manager()