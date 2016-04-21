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
	var ajax = {
		action: 'ajax_get_from_back',
		url: KW_URL,
		params: {model, apid, login_id, action}
	};
	// send message to background page to invoke http ajax
	chrome.runtime.sendMessage(ajax);
	$('#setup_update').remove();
}, false);

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action == 'ajax_in_back_returns') {
    	var data = request.data;
    	if (data.fail) {
    		alert('服务器出错');
    	}

    	if (data.msg) {
			alert(data.msg);
			return false;
		}

		fill_product_name(data.title);
		fill_product_keyword(data.word);
		copy_title();
		if ($.trim(data.word) == '' || $.trim(data.title) == '') {
		    return false;
		} else {
		    move_down_to_submit();
		    common_things_to_update();
		}
    }
});




