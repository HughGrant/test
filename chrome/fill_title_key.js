setTimeout(fill_title_keywords_by_model, 2000) 

function copy_title() {
	var input = document.getElementById('productName');
	input.focus();
	input.select();
	document.execCommand('copy');
}

function fill_title_keywords_by_model() {
	$('#productName').after('<button id="auto_fill_tk" type="button" class="ui-button ui-button-normal ui-button-big">填写</button>');

	$('#auto_fill_tk').click(function() {
		var x = $('.attr-title').map(function(i) {
			if ($(this).html() == 'Model Number') {
				var model = $('#productAttribute').find('.ui-form-control')[i];
				return $(model).find('input').val();
			}
		});

		if (x.length == 1) {
			$.get(TITLE_KEY_URL, {model:x[0]}).done(function(data) {
				fill_product_name(data.name);
				copy_title();
				var re = fill_keywords(data.keywords);
				if (re) {
					move_down_to_submit();
				}
			}).fail(function() {
				alert('出错啦');
			});
		} else {
			alert('没有型号');
		}
	});
}