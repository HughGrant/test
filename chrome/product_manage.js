$(function() {
	// has to be done in this way because of the product is load by ajax
	setInterval(detect_update, 1000);
});

function detect_update() {
	var list = $('.list-date');
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