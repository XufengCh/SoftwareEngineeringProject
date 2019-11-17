from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from HouseOfFashion import settings
# 如需测试存图请置为True
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
        with open(fname, 'wb') as pic:
            for c in image.chunks():
                pic.write(c)
    ret_dict = {'message': '服务器消息：图片已保存至数据库'}
    return JsonResponse(ret_dict)