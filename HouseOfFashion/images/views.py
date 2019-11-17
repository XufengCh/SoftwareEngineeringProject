from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from HouseOfFashion import settings
import os

# 如在上传图片时想要看到存在本地的图片请置为True
SAVE_UPLOAD = False

# upload_img():
# 用户更替主页图片时主动将图片存储到服务器中,根据用户发送图片的类型（type）来决定保存到拿一张表中
# TODO: 需要决定图片的hash值来唯一识别图片，并且标识要发送到前端

# 传入参数：
# pic(file)：对应用户上传的图片文件；通过request.FILES.get('pic')访问；
# type(bool)：为true则为衣服，false为半身像；request.POST.get('type')访问；
# name(string)：为用户电脑上的图片文件名

# 返回（json格式）：
# message(string)：前端弹出的信息
def upload_img(request):
    print(request.POST.get('name'))
    
    # 测试：可以正常地保存图片，存储目录 BASE_DIR\media\...
    if SAVE_UPLOAD:
        image = request.FILES.get('pic')
        fname = '%s%s' % (settings.MEDIA_ROOT, image.name)
        # 如果没有这个存储目录则为新建一个目录
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        with open(fname, 'wb') as pic:
            for c in image.chunks():
                pic.write(c)
    # 测试结束

    ret_dict = {'message': '[SERVER]图片已保存至数据库'}
    return JsonResponse(ret_dict)

# generate():
# 传入作为合成源的两张图片：衣物和用户的模特，调用对应接口进行图片生成并返回

# 传入参数：
# cloth(string)：用户选择的衣物对应的唯一标识；通过request.POST.get('cloth')访问；
# body(string)：用户选择的模特对应的唯一标识；request.POST.get('body')访问；

# 返回（json格式）：
# message(string)：前端弹出的信息
# result(file)：在前端展示的图片
# NOTE: 也可以考虑返回服务器上生成图片的地址
def generate(request):
    print('cloth: '+request.POST.get('cloth'))
    print('body: '+request.POST.get('body'))
    ret_dict = {'message': '[SERVER]图片合成已完成'}
    return JsonResponse(ret_dict)


# 试穿函数
def tryon(request):
    # 通过数据库操作得到前端的衣服和模特图片
    
    # 调用后端的试穿功能函数并得到效果图

    # 功能不完整时采用备用方案返回一张固定的图片

    # 思路一：把生成的图片也存放在服务器，返回图片的路径
    # 思路二：
    imagepath = path.join("media","default.jpg")
    print("imagepath="+str(imagepath))
    image_data = open(imagepath,"rb").read()
    return HttpResponse(image_data,content_type="image/jpg")

    # 思路三：生成的图片放数据库（看数据库那边的意思）


