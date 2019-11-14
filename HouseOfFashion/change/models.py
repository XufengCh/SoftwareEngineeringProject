from django.db import models
from ..images.models import Clothe, Body


# Create your models here.
class CompositeImage(models.Model):
    body = models.ForeignKey(to=Body, on_delete=models.CASCADE)
    clothe = models.ForeignKey(to=Clothe, on_delete=models.CASCADE)

    change_result = models.FileField(upload_to='composite-image/%Y/%m/%d')
