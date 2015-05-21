var get_delivery_cost = function(countryId, weight) {
    chrome.runtime.sendMessage({action:'delivery_cost', countryId:countryId, weight:weight});
}

var model_insert = function(model_name, data, success_msg, error_msg) {
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

var open_url = function(url) {
    chrome.runtime.sendMessage({action: 'open_url', url: url})
}

var download_url = function(url, filename) {
    chrome.runtime.sendMessage({
        action: 'download_url',
        url: url,
        filename: filename
    });
}

var collect_keywords = function(name) {
    chrome.runtime.sendMessage({action: 'collect_keywords', name: name});
}

var check_img = function(url) {
    open_url(url);
}