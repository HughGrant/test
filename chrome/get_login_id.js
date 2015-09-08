if (window.location.pathname.indexOf('products_manage') != -1) {
	send_and_track(MANAGEAPP.loginID)
}


if (window.location.pathname.indexOf('post_product_interface') != -1) {
	alert(POSTDATAMAP.loginID)
}

function send_and_track(id) {
	var evt = new CustomEvent('build', { 'detail': id });
	evt.initEvent("tracking_products", true, true);
	window.dispatchEvent(evt);
}