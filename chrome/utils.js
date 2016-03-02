// var jq = document.createElement('script');
// jq.src = "//cdn.bootcss.com/jquery/2.2.0/jquery.min.js";
// document.getElementsByTagName('head')[0].appendChild(jq);

function inject_script(file) {
    var th = document.getElementsByTagName('head')[0];
    var s = document.createElement('script');
    s.setAttribute('type', 'text/javascript');
    s.setAttribute('src', file);
    th.appendChild(s);
}

function open_url(url) {
    chrome.runtime.sendMessage({action: 'open_url', url: url})
}

function download_url(url, filename) {
    chrome.runtime.sendMessage({
        action: 'download_url',
        url: url,
        filename: filename
    });
}

function collect_keywords(name) {
    chrome.runtime.sendMessage({action: 'collect_keywords', name: name});
}

function download_images() {
    var name = get_product_name();
    var images = get_rich_text().imgs.concat(get_main_pictures());
    for (var i = images.length - 1; i >= 0; i--) {
        download_url(images[i], name + '.jpg');
    }
}

function check_img(url) {
    open_url(url);
}

function copy_title() {
    var input = document.getElementById('productName');
    input.focus();
    input.select();
    document.execCommand('copy');
}

function fill_product_name(name) {
    $('#productName').val(name);
}

function fill_product_keyword(keyword) {
    $('#productKeyword').val(keyword);
}

function fill_title_keyword_by_model(model) {
    $.get(KW_URL, {model: model}).done(function(data) {
        fill_product_name(data.title);
        fill_product_keyword(data.word);
        copy_title();
        if ($.trim(data.word) == '' || $.trim(data.title) == '') {
            return false;
        } else {
            move_down_to_submit();
        }
    }).fail(function() {
        alert('出错啦');
    });
}


function move_down_to_submit() {
    $('html, body').animate({
        scrollTop: $("#submitFormBtnA").offset().top
    }, 500);
}

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

function find_model() {
    var x = $('.attr-title').map(function(i) {
        if ($(this).html() == 'Model Number') {
            var model = $('#productAttribute').find('.ui-form-control')[i];
            return $(model).find('input').val();
        }
    });

    if (x.length == 1) {
        return x[0];
    } else {
        alert('没有填写型号或当前页面不是英文')
        return false;
    }
}