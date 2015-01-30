chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "upload_product") {
		upload_product(request.product);
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

    if (request.action == 'delivery_cost') {
        var countryId = request.countryId;
        var weight = request.weight;
        var url = 'http://183.62.161.176/custcenter/calculate!calculate.action?callback=&vo.packageType=2&vo.tempIds=0&vo.textileInd=N&vo.dbatteryInd=N&vo.dbatteryableInd=N&vo.pbatteryInd=N&vo.ybatteryInd=N&vo.cellphoneInd=N&vo.cbatteryInd=N&vo.poboxaddrInd=N&vo.telInd=Y&vo.oriInvoice=N&vo.longweightInd=N&vo.homeaddrInd=N&vo.tradedeclareInd=N&vo.countryId=' + countryId + '&vo.packageQty=1&vo.packageWeight=' + weight + '&vo.declarePrice=0&vo.recZipcode=&vo.recCity=&vo.vstring=' + weight + '%2C0%3B&_=' + time;
        $.get(url).done(function(data){
            console.log(data);
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

    if (request.action == 'upload_image') {
        
        var convert_img_to_base64 = function(url, callback, outputFormat) {
            var canvas = document.createElement('CANVAS');
            var ctx = canvas.getContext('2d');
            var img = new Image;
            img.crossOrigin = 'Anonymous';
            img.onload = function(){
                canvas.height = img.height;
                canvas.width = img.width;
                ctx.drawImage(img,0,0);
                var dataURL = canvas.toDataURL(outputFormat || 'image/jpeg');
                callback.call(this, dataURL);
                // Clean up
                canvas = null; 
            };
            img.src = url;
        }

        convert_img_to_base64(request.image_url, function(base64img) {
            chrome.tabs.sendMessage(sender.tab.id, {action:'upload_image', image:base64img, file_name:request.file_name});
            console.log(base64img);
        });
    }
})

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