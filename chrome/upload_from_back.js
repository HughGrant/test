document.addEventListener("upload_product", function(data) {
    var product = data.detail;
    product.from_back = true;
    chrome.runtime.sendMessage(
        {
            action: 'upload_product',
            product: product
        }
    );
}, false);