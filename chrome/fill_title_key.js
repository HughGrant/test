setTimeout(set_up_btn, 2000) 

function set_up_btn() {
	$('#productName').after('<button id="auto_fill_tk" type="button" class="ui-button ui-button-normal ui-button-big">填写</button>');

	$('#auto_fill_tk').click(function() {
		var model = find_model();
		if (model !== false) {
			fill_title_keyword_by_model(model)
		}
		// inject_script(chrome.extension.getURL('get_login_id.js'));
	});
}

// window.addEventListener("fill_product_title_keywords", function(data) {
// 	var email = ACCOUNT_ID_EMAIL_MAP[data.detail];
// 	if (email) {
// 	    fill_title_keywords_begin(email);
// 	} else {
// 		alert('帐户没有设置对应邮箱');
// 	}
// }, false)