setTimeout(setup_update, 1500) 

function setup_update() {
	$('#productName').after('<button id="setup_update" type="button" class="ui-button ui-button-normal ui-button-big">更新</button>');
	$('#setup_update').click(function() {
		inject_script(chrome.extension.getURL('get_login_id.js'));
	});
}

window.addEventListener("from_product_editing_page", function(data) {
	if (!data.detail) {
		alert('未能获取Login ID');
		return false;
	}

	var login_id = data.detail
	var model = find_model();
	if (model === false) {
		alert('没有型号');
	}

	var apid = get_apid();
	var action = 'update';
	var params = {model, apid, login_id, action};
	fill_tk_by_params(params);
	$('#setup_update').remove();
}, false)


// function update_all(email) {
// 	var model = find_model();
// 	if (model === false) {
// 		alert('没有型号');
// 		return false;
// 	}
// 	var apid = get_apid();
// 	var data ={model, apid};
// 	$.get(UPDATE_BY_MODEL, data).done(function(product) {
// 		if (!product.status) {
// 			alert(product.message);
// 			return false;
// 		}
// 		// update all
// 		var p = product.data;
// 		fill_product_name(p.name);
// 		var re = fill_keywords(p.keywords);
// 		if (re) {
// 			move_down_to_submit();
// 			auto_fill_product(p)
// 			auto_fill_rich_text(p)
// 		}
// 	}).fail(function() {
// 		alert('出错啦');
// 	});
// }