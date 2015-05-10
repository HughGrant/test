var html = '';
var current_li = false;

$(document).keydown(function(event) {
	
	if (event.ctrlKey) {
		if (event.keyCode == 81) {
			toggle_plate();
		}
	}

	if (event.keyCode == 27) {
		hide_plate();
	};
})

function set_up_plate() {
	if (html == '') {
		chrome.runtime.sendMessage({'action': 'command_plate'}, function(resp) {
			html = resp.html;
			$('body').append(html);
			hide_plate();
			fix_plate();
		});
	}
}

setTimeout(set_up_plate, 1000);

function toggle_plate() {
	$('#pp_plate').toggle();
	$('#cmd_field').focus();
}

function fix_plate() {
	var plate = $('#pp_plate');
	var w = $(window);
	plate.css('top', (w.height() / 2 - 180) + 'px');
	plate.css('left', (w.width() / 2 - 260) + 'px');
	var cmd_list = plate.find('li');
	cmd_list.hover(
		function() {
			current_li = parseInt(this.id);
			set_li(current_li);
		},
		function() {
			$(this).css('background-color', 'white');
			$(this).css('color', 'black');
		}
	);

	cmd_list.click(function() {
		var cmd = $(this).attr('cmd');
		exec_cmd(cmd);
	})

	$('#cmd_field').keyup(function(event) {
		var kw = event.keyCode;
		if (kw == 38 || kw == 40 || kw == 13) {
			return;
		}

		var str = $(this).val();
		var lis = $('#cmd_list li');
		if (str.length <= 0) { 
			current_li = false;
			lis.css('background-color', 'white').css('color', 'black');
			return; 
		}
		var cmds = {};
		lis.each(function() {
			cmds[$(this).attr('cmd')] = parseInt(this.id);
		});

		var t = 0.2;
		for (var cmd in cmds) {
			var s = cmd.score(str);
			if (s > t) {
				t = s;
				current_li = cmds[cmd];
				set_li(current_li);
			}
		}
	});

	$('#cmd_field').keydown(function(event) {
		var kw = event.keyCode;
		if (kw == 38) {
			li_move_up();
		}

		if (kw == 40) {
			li_move_down();
		}

		if (kw == 13) {
			var cmd = $('#cmd_list').find('li:eq(' + current_li + ')').attr('cmd');
			exec_cmd(cmd);
		}
	});
}

function exec_cmd(cmd) {
	if (cmd === 'upload product') {
		open_url(UPLOAD_PRODUCT_URL);
	} else if (cmd === 'search keyword') {
		open_url(SEARCH_HOT_KEYWORD_URL);
	}
}

function set_li(index) {
	var ul = $('#cmd_list');
	ul.find('li').css('background-color', 'white').css('color', 'black');
	var li = ul.find('li:eq(' + index + ')');
	li.css('background-color', '#0865bb').css('color', 'white');
	var page = Math.floor(index/10);
	ul.animate({scrollTop: page*311}, 500);
}

function li_move_up() {
	var count = $('#cmd_list').find('li').length;
	if (current_li === false || current_li <= 0) {
		current_li = count - 1;
	} else {
		current_li -= 1;
	}
	set_li(current_li);
}

function li_move_down() {
	var count = $('#cmd_list').find('li').length;
	if (current_li === false || current_li >= count - 1) {
		current_li = 0;
	} else {
		current_li += 1;
	}
	set_li(current_li);
}

function hide_plate() {
	$('#pp_plate').hide();
}