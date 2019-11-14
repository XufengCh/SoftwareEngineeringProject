from django.db import models
from users.models import User


# Create your models here.
class ClotheImage(models.Model):
    hash = models.CharField(max_length=40)
    image_file = models.FileField(upload_to='uploads/clothes/%Y/%m/%d')


class BodyImage(models.Model):
    hash = models.CharField(max_length=40)
    image_file = models.FileField(upload_to='uploads/bodys/%Y/%m/%d')


class Clothe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ForeignKey(to=ClotheImage, on_delete=models.CASCADE)


class Body(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ForeignKey(to=BodyImage, on_delete=models.CASCADE)