from django.db import models


# Create your models here.
from members.models import User


class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.Model)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    menu = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=50)
    image = models.ImageField(upload_to=True)
    link = models.ImageField(max_length=50)
