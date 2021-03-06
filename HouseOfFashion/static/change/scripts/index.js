const upload_url = "http://localhost:8000/images/upload_img";
const generate_url = "http://localhost:8000/images/generate";
$(document).ready(function () {
    // 用于标识当前选中图片的两个变量
    var clothe_selected = 0;
    var body_selected = 0;
    var clothe_id;
    var body_id;
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
    // 替换成功后将该图片发送到服务器后端添加到数据库中
    // ajax 发送的数据字典：
    // pic对应用户上传的图片文件；
    // type为true则为衣服，false为半身像；
    // name为用户电脑上的图片文件名
    // 注意因为使用 next(), prev() 组件的前后次序很重要
    $(".upload-img").on("change", function () {
        var container = String($(this).parents('.photo-wrapper').parent().attr('id'));
        
        let type = container.startsWith('clothe');
        let slot = Number(container.substring(container.length-1));
        let pic = this.files[0];
        let objUrl = getObjectURL(pic);
        
        var formdata=new FormData();
        formdata.append('slot',slot);
        formdata.append('pic',pic);
        formdata.append('type', type);
        
        $img = $(this).prev('.figure-img');
        // console.log(pic, type, slot);
        
        if (objUrl) {
            // 将图片路径存入src中，显示出图片
            $img.attr("src", objUrl); 
            // 向服务器发送数据字典
            $.ajax({
                // headers:{"X-CSRFtoken":$.cookie("csrftoken")},
                // headers: {"Access-Control-Allow-Origin":"*"},
                url: upload_url,
                type: "POST",
                data: formdata,
                dataType: "json",
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                processData: false,//用于对data参数进行序列化处理 这里必须false
                contentType: false, //必须
                success: function (data) {
                    console.log(data.message);
                    // console.log(pic.name + " 已成功保存到后端服务器");
                }
            });
        }
        // 将被框选的图片更改为当前用户替换的
        if (type) {
            $('#clothe-'+clothe_selected).removeClass('selected');
            $('#clothe-'+slot).addClass('selected');
            clothe_selected = slot;
        } else {
            $('#body-'+body_selected).removeClass('selected');
            $('#body-'+slot).addClass('selected');
            body_selected = slot;
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

    // 选择当前被选中的两张图片作为合成源
    // 在发送前先弹出窗口由用户确认
    $('#generate-btn').click(function (e) { 
        e.preventDefault();
        var source_cloth = $('#clothe-'+clothe_selected).find('.figure-img').attr('src');
        var source_body = $('#body-'+body_selected).find('.figure-img').attr('src');
        // TODO: 规定图片在数据库中的唯一标识
        // cloth_id = source_cloth; // FOR NOW
        // body_id = source_body; // FOR NOW
        
        var $modal = $('#submit-modal');
        $modal.modal('show');
        var source_cloth_pic = $modal.find('#source-cloth');
        source_cloth_pic.attr('src', source_cloth);
        var source_body_pic = $modal.find('#source-body');
        source_body_pic.attr('src', source_body);
        // TODO: set width
        // 现在先把宽度在html里面定死不改了
    });

   // 确认后将两张图片的标识发送给后端，并接收后端返回的合成结果
   // 用合成结果替换$('#display)中的图片
    $('#send-btn').click(function () { 
        // 向服务器发送数据字典
        let formdata = new FormData();
        formdata.append('cloth_slot', clothe_selected);
        formdata.append('body_slot', body_selected);
        $.ajax({
            type: "POST",
            url: generate_url,
            data: formdata,
            dataType: "json",
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data.message);
                $('#display img').attr('src', '/static/change/assets/sample-ash.jpg');
                // TODO: 替换生成图片框中的图片
                // console.log(data.result);
                // $('#display img').attr('src', getObjectURL(data.result));
            }
        });
        // 点击确认后关闭弹窗
        var $modal = $('#submit-modal');
        $modal.modal('hide');
    });
});

$(document).ajaxSend(function(event, jqxhr, settings) {
    if ( settings.url == generate_url ) {
        console.log("[CLIENT]图片合成ajax请求已发送");
        // TODO: ajax请求发出，图片合成时的加载动画 or 标志，让用户知道合成在进行
    }
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