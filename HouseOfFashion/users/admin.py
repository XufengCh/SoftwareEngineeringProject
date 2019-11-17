from django.contrib import admin
from .models import User
from change.models import CompositeImage
from images.models import ClotheImage, BodyImage, Clothe, Body

# Register your models here.
admin.site.register(User)
admin.site.register(Body)
admin.site.register(Clothe)
admin.site.register(BodyImage)
admin.site.register(ClotheImage)
admin.site.register(CompositeImage)

