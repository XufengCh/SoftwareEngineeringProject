from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('upload_img', views.upload_img, name='upload_img'),
    path('generate', views.generate, name='generate'),
]