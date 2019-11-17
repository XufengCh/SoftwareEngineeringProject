from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    # upload_img这个url不要修改
    path('upload_img', views.upload_img, name='upload_img'),
]