#!/usr/bin/env python
# coding=UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from images.models import *


def homepage(request):
    # template = loader.get_template('change/homepage.html')
    content = {}
    if request.user.is_authenticated:
        clothes = Clothe.objects.filter(user=request.user)      
        content['clothes'] = clothes
        # 测试证实可以通过.url得到前端访问图片使用的地址
        # print(clothes[0].image.image_file.url)
        bodies = Body.objects.filter(user=request.user)      
        content['bodies'] = bodies
    return render(request, 'change/index.html', content)
# Create your views here.
