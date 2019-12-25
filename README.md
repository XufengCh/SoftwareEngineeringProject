# SoftwareEngineeringProject
复旦大学软件工程化开发课程项目  

现在很多id和class名都和函数选择器绑定，不确定情况下尽量不要改  
负责后端开发的同学实现HouseOfFashion\images\views.py这个文件中的upload_img()和generate()两个函数

要求python版本3.7 
基于bootstrap4.0  
**pip install django-cors-headers**  
pip install numpy  
pip install opencv-python  
pip install pillow  
组件使用手册 https://getbootstrap.com/docs/4.0/components/alerts/  
据说在网站上看到的css格式比较准我之后再改  

执行命令 python manage.py runserver 
**访问http://localhost:8000/即可访问主页**  
注意先不要用127.0.0.1:8000 ajax会出问题   
不要把db.sqlite3的修改添加到项目里面   

管理员用户名 admin 
邮箱 499485532@qq.com 
密码 admin 
访问http://localhost:8000/admin 即可访问管理员页 

使用ajax与后端交互式使用了POST方法发送一个formdata 
在后端注释了csrf中间件（因为前端添加csrftoken失败） 
（理由不明）存在跨域访问问题，在后端添加了跨域中间件（settings.py），需要安装新组件（**见安装环境↑**）
