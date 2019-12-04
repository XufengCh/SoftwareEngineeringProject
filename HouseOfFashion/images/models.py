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
    """
    user: the user of the clothe
    image: the image of the clothe
    slot: 衣服在用户的界面中所显示的槽位
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ForeignKey(to=ClotheImage, on_delete=models.CASCADE)
    slot = models.PositiveSmallIntegerField()


class Body(models.Model):
    """
    user: the user of the body
    image: the image of the body
    slot: 半身照在用户的界面中所显示的槽位
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ForeignKey(to=BodyImage, on_delete=models.CASCADE)
    slot = models.PositiveSmallIntegerField()
