setTimeout(setup_update, 2000) 

function setup_update() {
	$('#productName').after('<button id="setup_update" type="button" class="ui-button ui-button-normal ui-button-big">更新标题与关键字</button>');
	$('#setup_update').click(function() {
		// inject_script(chrome.extension.getURL('get_login_id.js'));
		update_title_keyword();
		$('#setup_update').remove();
	});
}


// window.addEventListener("update_product_all", function(data) {
// 	var email = ACCOUNT_ID_EMAIL_MAP[data.detail];
// 	if (email) {
// 	    // $('#productName').after('<button id="update_all" type="button" class="ui-button ui-button-normal ui-button-big">全部</button>');
// 	    $('#productName').after('<button id="update_partial" type="button" class="ui-button ui-button-normal ui-button-big">部分</button>');
// 		$('#update_all').click(function() {
// 			update_all(email);
// 		});
// 		$('#update_partial').click(function() {
// 			update_partial(email);
// 		});
// 	} else {
// 		alert('帐户没有设置对应邮箱');
// 	}
// }, false)
function update_title_keyword(email) {
	var model = find_model();
	if (model === false) {
		alert('没有型号');
	} else {
		fill_title_keyword_by_model(model);
	}
}

function update_all(email) {
	var model = find_model();
	if (model === false) {
		alert('没有型号');
		return false;
	}
	var pid = window.location.search.split('=')[1];
	var data ={model, pid, email};
	$.get(UPDATE_BY_MODEL, data).done(function(product) {
		if (!product.status) {
			alert(product.message);
			return false;
		}
		// update all
		var p = product.data;
		fill_product_name(p.name);
		var re = fill_keywords(p.keywords);
		if (re) {
			move_down_to_submit();
			auto_fill_product(p)
			auto_fill_rich_text(p)
		}
	}).fail(function() {
		alert('出错啦');
	});
}