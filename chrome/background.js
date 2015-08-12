var plate_html = '';
var copy = '';
$.get(chrome.extension.getURL("plate.html"), function(data) {
    plate_html = data;
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "upload_product") {
		upload_product(request.product);
	}

    if (request.action == "copy_product") {
        copy = request.product;
        sendResponse({'status': true});
    }

    if (request.action == "paste_product") {
        sendResponse({'product': copy});
    }

    if (request.action == "command_plate") {
        sendResponse({'html': plate_html});
    }

    if (request.action == 'open_url') {
        chrome.tabs.create({url:request.url});
    }

    if (request.action == 'download_url') {
        chrome.downloads.download({
          url: request.url,
          filename: request.filename 
        });
    }

    if (request.action == 'collect_keywords') {
        chrome.tabs.create({'url':SEARCH_HOT_KEYWORD_URL}, function(tab) {
            chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, ctab) {
                if (tabId == tab.id && changeInfo.status == 'complete') {
                    chrome.tabs.sendMessage(tab.id, {action:'set_name', name:request.name});
                }
            });
        });
    }

});

var upload_product = function(record) {
    chrome.tabs.create({'url':UPLOAD_PRODUCT_URL}, function(tab) {
        chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, ctab) {
            if (tabId == tab.id && changeInfo.status == 'complete') {
                chrome.tabs.sendMessage(tab.id, {action:'set_product', product:record});
                chrome.tabs.sendMessage(tab.id, {action:'set_category', category:record.category});
            }
        });
    });
}