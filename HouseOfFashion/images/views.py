from django.core.files import File
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from HouseOfFashion import settings
from django.db import models
from images.models import *
from change.models import CompositeImage
from images.img_process import hash_md5


from .models import User
import sqlite3
import random
import time
import os
import sys
import math

import cv2
import numpy as np
from PIL import Image

# 如在上传图片时想要看到存在本地的图片请置为True
SAVE_UPLOAD = False
CLOTH_PATH = 'images/VirtualTryOn/data/raw_data/cloth/000001_1.jpg'
BODY_PATH = 'images/VirtualTryOn/data/raw_data/image/000001_0.jpg'
RESULT_PATH = 'images/VirtualTryOn/result/000001_0.jpg'

# upload_img():
# 用户更替主页图片时主动将图片存储到服务器中,根据用户发送图片的类型（type）来决定保存到拿一张表中
# TODO: 需要决定图片的hash值来唯一识别图片，并且标识要发送到前端

# 传入参数：
# pic(file)：对应用户上传的图片文件；通过request.FILES.get('pic')访问；
# type(bool)：为true则为衣服，false为半身像；request.POST.get('type')访问；
# slot(int)：前端图片对应的槽位，在表中唯一存在; request.POST.get('slot')访问；

# 返回（json格式）：
# message(string)：前端弹出的信息
def upload_img(request):
    # if request.user.is_authenticated:
    #     print(request.user.username + '用户已登录')
    # else:
    #     ret_dict = {'message': 'not authenticated'}
    #     return JsonResponse(ret_dict)
    system_message = ''
    # 测试：可以正常地保存图片，存储目录 BASE_DIR\media\...
    image = request.FILES.get('pic')
    slot = request.POST.get('slot')
    img_type = request.POST.get('type') == 'true'
    # 修改一下存图的文件名 “用户名-时分秒.文件类型”
    extension = str(image.name)[str(image.name).rfind('.'):]
    time_struct = time.localtime(time.time())
    str_time = time.strftime("%y%m%d%H%M%S", time_struct)
    str_username = request.user.username[:str(request.user.username).find('@')]
    fname = '%s%s-%s%s' % (settings.MEDIA_ROOT, str_username, str_time, extension)
    image.name = fname

    if img_type:
        print(request.user.username + ": NEW IMAGE IN CLOTHE SLOT " + slot)
    else:
        print(request.user.username + ": NEW IMAGE IN BODY SLOT " + slot)


    # 可以存进数据库之后这块就不用执行了
    if SAVE_UPLOAD:
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        with open(fname, 'wb') as pic:
            for c in image.chunks():
                pic.write(c)
    print(image.name, " hash value-> ", hash_md5(image))
    # print(request.user.is_authenticated)
    # print(request.user.username)
    if img_type:
        # 如果数据库中已存在就不插入新纪录
        try:
            clothe_image = ClotheImage.objects.get(hash=hash_md5(image))
        except ClotheImage.DoesNotExist:
            clothe_image = ClotheImage.objects.create(    #数据库插入语句
                hash=hash_md5(image),
                image_file=image,
            )
        # 删除用户在这个槽位上的记录
        try:
            Clothe.objects.get(slot=slot).delete()
            print(request.user.username + ": DELETE OLD IMAGE IN CLOTHE SLOT " + slot)
        except Clothe.DoesNotExist:
            pass
        
        Clothe.objects.create(
            user=request.user,
            image=clothe_image,
            slot=slot
        )
    else:
        try:
            body_image = BodyImage.objects.get(hash=hash_md5(image))
        except BodyImage.DoesNotExist:
            body_image = BodyImage.objects.create(    #数据库插入语句
                hash=hash_md5(image),
                image_file=image,
            )

        # 删除用户在这个槽位上的记录
        try:
            Body.objects.get(slot=slot).delete()
            print(request.user.username + ": DELETE OLD IMAGE IN BODY SLOT " + slot)
        except Body.DoesNotExist:
            pass
        
        Body.objects.create(
            user=request.user,
            image=body_image,
            slot=slot
        )
    # 测试结束

    ret_dict = {'message': '[SERVER]图片已保存至数据库'}
    return JsonResponse(ret_dict)

# generate():
# 传入作为合成源的两张图片：衣物和用户的模特，调用对应接口进行图片生成并返回
# 根据传入的两个槽号查找Cloth，Body表得到image文件
# 再利用两个文件查找合成表，若记录存在则返回已有结果，记录不存在进行合成并插入新记录

# 传入参数：
# cloth_slot(int)：用户选择的衣物对应的唯一标识；通过request.POST.get('cloth')访问；
# body_slot(int)：用户选择的模特对应的唯一标识；request.POST.get('body')访问；

# 返回（json格式）：
# message(string)：前端弹出的信息
# result(string)：返回CompositeImageObject.composite_image.url
def generate(request):
    clothe_slot = request.POST.get('cloth_slot')
    body_slot = request.POST.get('body_slot')
    print('[SERVER] GENERATE: CLOTH SLOT ' + clothe_slot)
    print('[SERVER] GENERATE: BODY SLOT ' + body_slot)

    try:
        clothe = Clothe.objects.get(user=request.user, slot=clothe_slot)
        body = Body.objects.get(user=request.user, slot=body_slot)
        # print(clothe)
    except (Clothe.DoesNotExist, Body.DoesNotExist):
        ret_dict = {'message': 'not found'}
        return JsonResponse(ret_dict)

    results = CompositeImage.objects.filter(clothe_image=clothe.image, body_image=body.image)
    # (1)检查是否已经生成 （2.1）若已生成则直接从数据库中得到
    # (2.2)若未生成则先进行图片合成，存储在服务器上再存入数据库中
    # (3)返回图片地址

    if len(results) == 0:

        # 1 保存路径
        clothe_img = Image.open(clothe.image.image_file)
        body_img = Image.open(body.image.image_file)
        clothe_img.save(CLOTH_PATH)
        body_img.save(BODY_PATH)

        # 2 调用合成函数
        cur_dir = os.getcwd()
        print(cur_dir)
        os.chdir("images/VirtualTryOn/")
        os.system("python try_on.py")
        os.chdir(cur_dir)

        # 3 从result路径读取结果
        f = RESULT_PATH
        comp_res = CompositeImage.objects.create(
            body_image=body.image,
            clothe_image=clothe.image,
            composite_image=File(open(f, 'rb'))
        )
    else:
        # NOTE: 防止前端过快得到结果来不及隐藏waitModal
        time.sleep(1)
        comp_res = results[0]
    
    ret_dict = {'message': '[SERVER]图片合成已完成 FINISHED!',
                'result': comp_res.composite_image.url }
                # 'result': '/static/change/assets/sample-ash.jpg'}
    return JsonResponse(ret_dict)

# evaluate():
# 用户登录才能使用的功能
# 根据传入的两个槽号查找Cloth，Body表得到image文件
# 再利用两个文件查找合成表，若记录存在对合成图片进行评价并返回结果，记录不存在提醒用户先进行合成

# 传入参数：
# cloth_slot 用于合成该图片的衣物槽号
# body_slot 用于合成该图片的姿态槽号

# 返回（json格式）：
# message(string)：前端弹出的信息
# score(string)：合成图片对应的评分


def image_colorfulness(image):
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.absolute(R - G)
    yb = np.absolute(0.5 * (R + G) - B)
    #平均值 标准差
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    std = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    mean = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # 返回颜色丰富度C
    return math.sqrt(math.sqrt(std + (0.3 * mean)) * 10) * 10


def evaluate(request):
    clothe_slot = request.POST.get('clothe_slot')
    body_slot = request.POST.get('body_slot')
    clothe = Clothe.objects.get(user=request.user, slot=clothe_slot)
    body = Body.objects.get(user=request.user, slot=body_slot)
    results = CompositeImage.objects.filter(clothe_image=clothe.image, body_image=body.image)
    composite_image = Image.open(results[0].composite_image)  # 如果表中没有对应记录会有 IndexOutOfRange
    # 先把用户合成记录最后一次的图片拿出来存到服务器上，再从服务器利用cv2.imread读入
    print('**********')
    print(composite_image)
    composite_image.save(RESULT_PATH)
    print('1**********')
    composite_image = cv2.imread(RESULT_PATH)
    print('2**********')
    score = image_colorfulness(composite_image)
    print(score)
    print('3**********')
    ret_dict = {'message': '[SERVER]评分结果已返回',
                'score': score}
    try:
        clothe_slot = request.POST.get('clothe_slot')
        body_slot = request.POST.get('body_slot')
        clothe = Clothe.objects.get(user=request.user, slot=clothe_slot)
        body = Body.objects.get(user=request.user, slot=body_slot)
        results = CompositeImage.objects.filter(clothe_image=clothe.image, body_image=body.image)
        composite_image = Image.open(results[0].composite_image)  # 如果表中没有对应记录会有 IndexOutOfRange
        # 先把用户合成记录最后一次的图片拿出来存到服务器上，再从服务器利用cv2.imread读入
        print('**********')
        print(composite_image)
        composite_image.save(RESULT_PATH)
        print('1**********')
        composite_image = cv2.imread(RESULT_PATH)
        print('2**********')
        score = image_colorfulness(composite_image)
        print(score)
        print('3**********')
        ret_dict = {'message': '[SERVER]评分结果已返回',
                'score': score}
    except Exception:
        ret_dict = {'message': 'not found'}

    return JsonResponse(ret_dict)

# 试穿函数
def tryon(request):
    # 通过数据库操作得到前端的衣服和模特图片
    
    # 调用后端的试穿功能函数并得到效果图

    # 功能不完整时采用备用方案返回一张固定的图片

    # 思路一：把生成的图片也存放在服务器，返回图片的路径
    # 思路二：
    imagepath = os.path.join("media","default.jpg")
    print("imagepath="+str(imagepath))
    image_data = open(imagepath,"rb").read()
    return HttpResponse(image_data,content_type="image/jpg")

    # 思路三：生成的图片放数据库（看数据库那边的意思）

def test(request):
    print(request.session)
    if request.user.is_authenticated:
        print("已登录")
    return redirect('/')


