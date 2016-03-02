setInterval(detect_update, 2000);
// setInterval(tracking_products, 2000);

function detect_update() {
	var list = $('.manager-list-col-updated');
	if (list.length == 0) {
		return false;
	}

	list.map(function(index) {
		var list_date = $(this);
        if (list_date.hasClass('reminded')) { return false; };
		list_date.addClass('reminded');

		var	date = $.trim(list_date.find('span:eq(0)').text());
		// English time format day/month/year
		if (date.indexOf('/') != -1) {
			date = date.split('/').reverse().join('-');
		}
		date = (new Date(date)).valueOf();
		var now = (new Date()).valueOf();
		var days = Math.round((now - date)/86400000);

		if (days >= 7) {
            var reminder = '<br><span style="color:#FFF;background-color:#F60;">' + days + '天没有更新</span>';
			list_date.find('span:eq(1)').append(reminder);
		}
	});
}

// function tracking_products() {
// 	if ($('#tp_btn').length == 0) {
// 		var btn = '<a id="tp_btn" class="ui2-button ui2-button-default ui2-button-normal ui2-button-small" title="">Tracking Products</a>';
// 		$('.manage-action-buttons').append(btn);

// 		$('#tp_btn').click(function() {
// 			inject_script(chrome.extension.getURL('get_login_id.js'));
// 		});
// 	}
// }

// window.addEventListener("tracking_products", function(data) {
// 	var email = ACCOUNT_ID_EMAIL_MAP[data.detail];
// 	if (email) {
// 	    collect_product_list(email);
// 	} else {
// 		alert('帐户没有设置对应邮箱');
// 	}
// }, false)

// function collect_product_list(account) {
// 	var ids = [];
// 	var titles = [];
// 	$('.manager-list-col-title>a').map(function() {
// 		var id = $(this).attr('href').split('id=')[1];
// 		var title = $(this).attr('title')
// 		titles.push(title);
// 		ids.push({account: account, pid: id, title: title, model: ''});
// 	});

// 	// detect duplicate titles
// 	titles = titles.sort()
// 	for (var i = 0; i < titles.length - 1; i++) {
// 		if (titles[i + 1] === titles[i]) {
// 			alert('重复标题:' + titles[i]);
// 			return false;
// 		}
// 	}

// 	var models = []
// 	$('.icon-list>i').map(function() {
// 		models.push($.trim($(this).html().replace('(', '').replace(')', '')));
// 	});

// 	if (ids.length != models.length) {
// 		alert('长度不一致');
// 		return false;
// 	}

// 	models.forEach(function(m, i) {
// 		ids[i].model = m;
// 	});

// 	data = {'json': JSON.stringify(ids)}
// 	$.post(TRACKING_LIST_URL, data).done(function(data) {
// 		if (data.status) {
// 			alert(data.msg)
// 		}
// 	}).fail(function() {
// 		alert('server error');
// 	});
// }