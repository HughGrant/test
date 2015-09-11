setTimeout(set_up_btn, 2000) 

function set_up_btn() {
	$('#productName').after('<button id="auto_fill_tk" type="button" class="ui-button ui-button-normal ui-button-big">填写</button>');

	$('#auto_fill_tk').click(function() {
		inject_script(chrome.extension.getURL('get_login_id.js'));
	});
}

window.addEventListener("fill_product_title_keywords", function(data) {
	var email = ACCOUNT_ID_EMAIL_MAP[data.detail];
	if (email) {
	    fill_title_keywords_begin(email);
	} else {
		alert('帐户没有设置对应邮箱');
	}
}, false)

function fill_title_keywords_begin(email) {
	var x = $('.attr-title').map(function(i) {
		if ($(this).html() == 'Model Number') {
			var model = $('#productAttribute').find('.ui-form-control')[i];
			return $(model).find('input').val();
		}
	});

	if (x.length == 1) {
		fill_title_keywords_by_email_model(email, x[0])
	} else {
		alert('没有型号');
	}
}