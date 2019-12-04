from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from HouseOfFashion import settings
from django.db import models
from images.models import *
from images.img_process import hash_md5
from .models import User
import sqlite3
import os

# 如在上传图片时想要看到存在本地的图片请置为True
SAVE_UPLOAD = False

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
    # test
    # if request.user.is_authenticated:
    #     print(request.user.username + '用户已登录')
    # else:
    #     print('LOGIN FAILED')
    system_message = ''
    # 测试：可以正常地保存图片，存储目录 BASE_DIR\media\...
    image = request.FILES.get('pic')
    fname = '%s%s' % (settings.MEDIA_ROOT, image.name)
    slot = request.POST.get('slot')
    img_type = request.POST.get('type') == 'true'
    if img_type:
        print(request.user.username + ": NEW IMAGE IN CLOTHE SLOT " + request.POST.get('slot'))
    else:
        print(request.user.username + ": NEW IMAGE IN BODY SLOT " + request.POST.get('slot'))


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
            print(request.user.username + ": DELETE OLD IMAGE IN CLOTHE SLOT " + request.POST.get('slot'))
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
            print(request.user.username + ": DELETE OLD IMAGE IN BODY SLOT " + request.POST.get('slot'))
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

# 传入参数：
# cloth_slot(int)：用户选择的衣物对应的唯一标识；通过request.POST.get('cloth')访问；
# body_slot(int)：用户选择的模特对应的唯一标识；request.POST.get('body')访问；

# 返回（json格式）：
# message(string)：前端弹出的信息
# result(file)：在前端展示的图片
# NOTE: 也可以考虑返回服务器上生成图片的地址
def generate(request):
    print('clothSlotNumber: '+request.POST.get('cloth_slot'))
    print('bodySlotNumber: '+request.POST.get('body_slot'))
    clothe_image=ClotheImage.image_file
    ret_dict = {'message': '[SERVER]图片合成已完成'}
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


