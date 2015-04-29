var html = '';
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
	plate.css('top', (w.height() / 2 - 100) + 'px');
	plate.css('left', (w.width() / 2 - 260) + 'px');

	plate.find('li').hover(
		function() {
			$(this).css('background-color', '#0865bb');
			$(this).css('color', 'white');
		},
		function() {
			$(this).css('background-color', 'white');
			$(this).css('color', 'black');
		}
	);

	$('#cmd_field').keyup(function(event) {
		console.log($(this).val());
	});

	$('#cmd_field').keydown(function(event) {
		if (event.keyCode == 38) {
			li_move_up();
		}

		if (event.keyCode == 40) {
			li_move_down();
		}
	});
}

var current_li = 0;

function set_li(index) {
	var ul = $('#cmd_list');
	ul.find('li').css('background-color', 'white').css('color', 'black');
	var li = ul.find('li:eq(' + index + ')');
	li.css('background-color', '#0865bb').css('color', 'white');
	var page = Math.floor(index/10);
	ul.animate({scrollTop: page*311}, 100);
}

function li_move_up() {
	var count = $('#cmd_list').find('li').length;
	current_li -= 1;
	if (current_li < 0) {
		current_li = count;
	}
	set_li(current_li - 1);
}

function li_move_down() {
	var count = $('#cmd_list').find('li').length;
	current_li += 1
	if (current_li > count) {
		current_li = 1;
	}
	set_li(current_li - 1);
}

function hide_plate() {
	$('#pp_plate').hide();
}