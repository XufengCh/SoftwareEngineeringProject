const upload_url = "http://localhost:8000/images/upload_img";
const generate_url = "http://localhost:8000/images/generate";
const evaluate_url = "http://localhost:8000/images/evaluate";
$(document).ready(function () {
    // 用于标识当前选中图片的两个变量
    var clothe_selected = 0;
    var body_selected = 0;
    var clothe_id;
    var body_id;
    var type;
    var slot;
    var filename;
    // 保留结果两位小数
    const roundup = 2;
    // 用于规定可选栏位最大最小值的两个常量
    const clothe_max = 5;
    const body_max = 5;
    // 初始化裁剪组件
    $imageToCrop = $('#source-img');
    $imageToCrop.cropper({  
        aspectRatio : 4 / 5,// 默认比例  
        guides: true, // 裁剪框的虚线(九宫格)  
        zoomable : false,
        minContainerWidth: 400,
        minContainerHeight: 400,
        crop : function(e) {  
            // 输出结果数据裁剪图像。  
        }  
    });
    
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
    $(".upload-img").on("change", function () {
        var container = String($(this).parents('.photo-wrapper').parent().attr('id'));
        let pic = this.files[0];
        console.log(pic);
        let objUrl = getObjectURL(pic);
        type = container.startsWith('clothe');
        slot = Number(container.substring(container.length - 1));
        filename = pic.name;

        // 唤醒modal让用户进行图片裁剪,替换modal中的被裁减图片
        $("#crop-modal").modal('show');
        $imageToCrop.cropper('replace', objUrl);// 默认false，适应高度，不失真  
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

    // 用户裁剪完成后按下确认执行
    // 替换成功后将该图片发送到服务器后端添加到数据库中
    // ajax 发送的数据字典：
    // pic对应用户上传的图片文件；
    // type为true则为衣服，false为半身像；
    // name为用户电脑上的图片文件名
    $("#sure-cut-btn").on("click", function(){
        if ($("#source-img").attr("src") == null) {  
            return false;  
        } else {  
            var cas = $('#source-img').cropper('getCroppedCanvas');// 获取被裁剪后的canvas  
            var pic = cas.toDataURL('image/jpeg'); // 转换为base64图片文件
            // 重新创建一个新的FILE对象
            data=pic.split(',')[1];
            data=window.atob(data);
            var ia = new Uint8Array(data.length);
            for (var i = 0; i < data.length; i++) {
                ia[i] = data.charCodeAt(i);
            }
            var croppedPic = new File([ia], filename, { type: "image/jpeg", endings: 'transparent' });
            console.log(croppedPic);
            // 选择器选出之前的那个图片框,用裁剪后的图片替换
            var selector;
            if (type) {
                selector = '#clothe-' + slot + ' .figure-img';
            } else {
                selector = '#body-' + slot + ' .figure-img';
            }
            // console.log(selector);
            $imageSlot = $(selector);
            $imageSlot.attr("src", pic);// 显示图片
            // 内容上传服务器
            var formdata=new FormData();
            formdata.append('slot',slot);
            formdata.append('pic', croppedPic);
            formdata.append('type', type);
            formdata.append('filename', filename);
            
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
                }
            });
            $('#crop-modal').modal('hide');
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
    $('#generate-btn').on("click", function (e) { 
        e.preventDefault();
        var source_cloth = $('#clothe-'+clothe_selected).find('.figure-img').attr('src');
        var source_body = $('#body-'+body_selected).find('.figure-img').attr('src');
        
        var $modal = $('#submit-modal');
        $modal.modal('show');
        var source_cloth_pic = $modal.find('#source-cloth');
        source_cloth_pic.attr('src', source_cloth);
        var source_body_pic = $modal.find('#source-body');
        source_body_pic.attr('src', source_body);
    });

   // 确认后将两张图片的标识发送给后端，并接收后端返回的合成结果
   // 用合成结果替换$('#display)中的图片
    $('#send-btn').on("click", function () { 
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
                // TODO: 替换生成图片框中的图片
                console.log(data.result);
                $('#display img').attr('src', data.result);
            }
        });
        // 点击确认后关闭弹窗
        var $modal = $('#submit-modal');
        $modal.modal('hide');
    });

    // 评价用户当前的合成结果
    // 当前设计只能显示用户的一次合成结果，因此不需要发送任何参数，服务器查找用户最后一次合成记录即可
    $('#eval-btn').on("click", function () {
        // console.log("eval-btn onclick");
        $.ajax({
            type: "POST",
            url: evaluate_url,
            dataType: "json",
            data: {
                'clothe_slot': clothe_selected,
                'body_slot': body_selected
            },
            success: function (response) {
                console.log(response.message);
                if (response.message == 'not found') {
                    alert("请先合成图片");
                }
                else {
                    dot = String(response.score).indexOf(".");
                    score = String(response.score).substring(0, dot + roundup + 1);
                    $('#score').html(score);
                }
            }
        });
    });

    // 用户与download-btn交互时执行，新建一个a节点触发click事件
    $('#download-btn').on("click", function (param) {
        var $download_img = $('#display img');
        var url = $download_img.attr('src');
        var a = document.createElement('a');
        var event = new MouseEvent('click');
        a.download = 'generated image';
        a.href = url;
        console.log(url);
        a.dispatchEvent(event);
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