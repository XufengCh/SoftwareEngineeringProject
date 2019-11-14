$(document).ready(function () {
    // 用于标识当前选中图片的两个变量
    var clothe_selected = 0;
    var body_selected = 0;
    // 用于规定可选栏位最大最小值的两个常量
    const clothe_max = 5;
    const body_max = 5;
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

    //在点击左右按钮时切换当前选中的衣物/模特图片
    //函数绑定在类arr-btn上，再根据组件的id进行左右位移操作，为对应的图片添加selected类
    $(".arr-btn").on("click", function(){
        var arr_type = $(this).attr('id');
        // alert(arr_type);
        $('#clothe-'+clothe_selected).removeClass('selected');
        $('#body-'+body_selected).removeClass('selected');
        switch (arr_type) {
            case 'clothes-left-arrow':
                if(clothe_selected > 0) clothe_selected--;
                break;
            case 'clothes-right-arrow':
                if(clothe_selected < clothe_max-1) clothe_selected++;
                break;
            case 'bodies-left-arrow':
                if(body_selected > 0) body_selected--;
                break;
            case 'bodies-right-arrow':
                if(body_selected < body_max-1) body_selected++;
                break;
            default:
                alert("有人改了我的箭头ID");
                break;
        }
        $('#clothe-'+clothe_selected).addClass('selected');
        $('#body-'+body_selected).addClass('selected');
    });

    $('#generate-btn').click(function (e) { 
        e.preventDefault();
        var source_cloth = $('#clothe-'+clothe_selected).find('.figure-img').attr('src');
        var source_body = $('#body-'+body_selected).find('.figure-img').attr('src');
        // alert(source_body);
        // alert(source_cloth);
        var $modal = $('#submit-modal');
        $modal.modal('show');
        var source_cloth_pic = $modal.find('#source-cloth');
        source_cloth_pic.attr('src', source_cloth);
        var source_body_pic = $modal.find('#source-body');
        source_body_pic.attr('src', source_body);
        // TODO: set width
        // 现在先把宽度在html里面定死不改了
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