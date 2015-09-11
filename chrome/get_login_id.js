if (window.location.pathname.indexOf('products_manage') != -1) {
	var evt = new CustomEvent('build', {'detail': MANAGEAPP.loginID});
	evt.initEvent("tracking_products", true, true);
	window.dispatchEvent(evt);
}


if (window.location.pathname.indexOf('post_product_interface') != -1) {
	var evt = new CustomEvent('build', {'detail': POSTDATAMAP.loginId});
	evt.initEvent("fill_product_title_keywords", true, true);
	window.dispatchEvent(evt);
}

if (window.location.pathname.indexOf('posting') != -1) {
	var evt = new CustomEvent('build', {'detail': POSTDATAMAP.loginId});
	evt.initEvent("upload_from_back", true, true);
	window.dispatchEvent(evt);
}