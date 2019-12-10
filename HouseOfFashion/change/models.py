from django.db import models
from images.models import ClotheImage, BodyImage


# Create your models here.
class CompositeImage(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    body_image = models.ForeignKey(to=BodyImage, on_delete=models.CASCADE)
    clothe_image = models.ForeignKey(to=ClotheImage, on_delete=models.CASCADE)

    composite_image = models.FileField(upload_to='composite-image/%Y/%m/%d')
    score = models.CharField(max_length=10)
