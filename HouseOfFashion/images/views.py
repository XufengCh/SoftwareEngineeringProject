from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
# 用户更替主页图片时主动将图片存储到服务器中
def upload_img(request):
    print(request.POST.get('name'))
    ret_dict = {'message': '成功保存'}
    return JsonResponse(ret_dict)