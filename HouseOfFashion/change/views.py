#!/usr/bin/env python
# coding=UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def homepage(request):
    # template = loader.get_template('change/homepage.html')
    return render(request, 'change/homepage.html')
# Create your views here.
