$(document).ready(function () {
    // DEBUG: 在figure-img的on-click函数里调用这个函数会调用到爆栈
    // 原因不清楚先这么处理
    $('.upload-img').on('click', function (e) {
        // alert('clicked!');
        e.stopPropagation();
    });

    // 点击照片使触发input-image组件，允许用户上传图片
    // 注意因为使用 next(), prev() 组件的前后次序很重要
    $('.figure-img').click(function (e) {
        $upload = $(this).next('.upload-img');
        $upload.trigger('click');
    });

    // 用户上传图片结束后组件内容改变，调用getObjectURL()得到可用地址，替换与此组件相邻的图片的src属性
    // 注意因为使用 next(), prev() 组件的前后次序很重要
    $(".upload-img").on("change", function () {
        var objUrl = getObjectURL(this.files[0]); 
        // DEBUG用地址弹窗
        // alert(objUrl);
        $img = $(this).prev('.figure-img');
        if (objUrl) {
            //将图片路径存入src中，显示出图片
            $img.attr("src", objUrl); 
        }
    });
});

//获取图片的路径，该路径不是图片在本地的路径
function getObjectURL(file) {
    var url = null;
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}