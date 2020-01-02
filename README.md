# SoftwareEngineeringProject
复旦大学软件工程化开发课程项目  

## Installation
* Clone this project to your directory.
* 要求python版本3.7 
* 基于bootstrap4.0  
* Install Virtual-try-on part according to **试穿模块配置**
```
pip install django-cors-headers 
pip install numpy  
pip install opencv-python  
pip install pillow  
```
组件使用手册 https://getbootstrap.com/docs/4.0/components/alerts/

## Usage
执行命令 python manage.py runserver 
**访问http://localhost:8000/即可访问主页**  
注意先不要用127.0.0.1:8000 ajax会出问题   
不要把db.sqlite3的修改添加到项目里面   

管理员用户名 admin 
邮箱 499485532@qq.com 
密码 admin 
访问http://localhost:8000/admin 即可访问管理员页 
现在很多id和class名都和函数选择器绑定，不确定情况下尽量不要改  

使用ajax与后端交互式使用了POST方法发送一个formdata 
在后端注释了csrf中间件（因为前端添加csrftoken失败） 
（理由不明）存在跨域访问问题，在后端添加了跨域中间件（settings.py），需要安装新组件（**见安装环境↑**）

## 试穿模块配置

### 环境安装
* Tensorflow 1.13.1
* Pytorch 1.3.0
* torchvision 0.2.1
* python 3.6.5
* MATLAB 2018b
* Download [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to the```HouseOfFashion\images\VirtualTryOn\OpenPose``` directory and compile it according to its instruction.
* Download pre-trained model for [JPPNet](https://github.com/Engineering-Course/LIP_JPPNet) and put it under ```HouseOfFashion\images\VirtualTryOn\LIP_JPPNet/checkpoint/JPPNet-s2/```. There should be 4 files in this directory: checkpoint, model.ckpt-xxx.data-xxx, model.ckpt-xxx.index, model.ckpt-xxx.meta.
* Download pre-trained models for [cp-vton](https://github.com/sergeywong/cp-vton) and put them under ```HouseOfFashion\images\VirtualTryOn\cp_vton/checkpoints/```. There should be two folders as ```gmm_train_new``` and ```tom_train_new``` in this directory. The authors have not provided the original models but you may download the models from [a re-implemented one](https://github.com/cinastanbean/cp-vton).

