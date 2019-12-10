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
        # for pic_type in ['clothe-', 'body-']:
        # TODO: 这里把查询改一下前端的django过滤器就可以写成循环了
        for slot in [0, 1, 2, 3, 4]:
            try:
                clothe = Clothe.objects.get(user=request.user, slot=slot)      
                content['clothe' + str(slot)] = clothe
            except Clothe.DoesNotExist:
                pass
        for slot in [0, 1, 2, 3, 4]:
            try:
                body = Body.objects.get(user=request.user, slot=slot)      
                content['body' + str(slot)] = body
            except Body.DoesNotExist:
                pass        
    return render(request, 'change/index.html', content)
# Create your views here.
