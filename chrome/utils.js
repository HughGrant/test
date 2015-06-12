function model_insert(model_name, data, success_msg, error_msg) {
    $.ajax({
        url: DOMAIN + model_name,
        data: JSON.stringify(data),
        type: 'POST',
        success: function(data) {
            alert(success_msg)
        },
        error: function(data) {
            alert(error_msg)
        }
    })
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