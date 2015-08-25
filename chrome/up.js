var product = null;

function add_more_attr(key, value) {
	var cai = $('.custom-attr-item').last();
	cai.find('input').first().val(key);
	cai.find('input').last().val(value);
	$('#copyActionButton').click();
}

// no sign of use of this function yet
function select_by_val(elem, val) {
	var name = elem.attr('name');
	$('[name=' + name + ']').val(val);
}

function create_other_input(name, value) {
	// this function is used to create a input box which should be
	// visible on the page after you select a "other" value
	var input_name = 'otherAttrContext' + name.replace('sysAttrValueIdAndValue', '');
	var input = '<input value="' + value + '" id="" name="' + input_name + '" type="text" class="ui-textfield ui-textfield-system ui-control-m">';
	return input;
}

function select_by_text(elem, text) {
	var name = elem.find('select').attr('name');
	var option = $('[name=' + name + '] option').filter(function() {
		return ($(this).text() == text);
	});

	if (option.length) {
		option.prop('selected', true);
	} else {
		$('[name=' + name + '] option').filter(function() {
			return ($(this).text() == 'Other')
		}).prop('selected', true);
		var input = create_other_input(name, text);
		elem.append(input);
	}
}

function check_payment_box(values) {
	values.map(function(v) {
		var v = $.trim(v);
		var input = $('input[value="' + v + '"]');
		if (input) {
			input.prop('checked', true);
		} else {
			$('#paymentMethodOther').prop('checked', true);
			var pm = $('#paymentMethodOtherDesc');
			var pre = pm.val();
			var now = pre + ',' + 'v';
			pm.val(now);
		}
	})
}

function check_box(elem, values) {
	// elem = $(elem);
	// get all available default options 
	var defaults = elem.find('label').map(function() {
		return $(this).text().trim();
	});

	var left = [];
	for (var i = values.length - 1; i >= 0; i--) {
		var find = false;
		for (var j = defaults.length - 1; j >= 0; j--) {
			if (values[i] == defaults[j]) {
				find = true;
				elem.find('input:eq(' + j + ')').prop('checked', true);
				break;
			}
		}
		if (find == false) {
			left.push(values[i]);
		}
	}

	if (left.length != 0) {
		var other = elem.find('input:eq(0)');
		var name = other.attr('name');
		var input = create_other_input(name, left.join(', '));
		other.prop('checked', true);
		// where to put it
		elem.find('ul').after(input);
	}
}

function fill_attr(elem, val) {
	var elem = $(elem);
	if (elem.find('input[type=text]').size() > 0) {
		elem.find('input').val(val);
	} else if (elem.find('select').size() > 0) {
		select_by_text(elem, val);
	} else if (elem.find('input[type=checkbox]').size() > 0) {
		check_box(elem, val.split(','));
	}
}

function mark_empty_attr(elem) {
	// could be one of the following
	$(elem).find('input[type=text]').css('border', '2px solid red');
	$(elem).find('select').css('border', '2px solid red');
	$(elem).find('input[type=checkbox]').css('border', '2px solid red');
}

function fill_keywords(product) {
	if (product.keywords.length < 3) {
		collect_keywords(product.basic_id);
		return;
	}

	$('#addMoreKeywords').remove();
	$('#smk-more-keywords-wrapper').show();
	
	var key1 = $('#productKeyword'),
    	key2 = $('#keywords2'),
    	key3 = $('#keywords3');

	key1.val(product.keywords.shift());
    key2.val(product.keywords.shift());
    key3.val(product.keywords.shift());
}

function paste_product() {
	chrome.runtime.sendMessage({'action': 'paste_product'}, function(resp) {
		var temp = resp.product;
		if (temp === '') {
			alert('请先复制产品');
			return;
		}
		auto_fill_product(temp);
	});
}

function auto_fill_product(product) {
	// find out what lang that this page is in
	var is_en = $('.ui-header-lan-display-text').html() == 'English';
	if (!is_en) {
		alert('请先把页面语言设置为英文');
		return false;
	}
	// set up inital state for all product attr list
	for (var i = product.attrs.length - 1; i >= 0; i--) {
		product.attrs[i][2] = false;
	}

	product.get_attr_val = function(key) {
		for (var i = 0; i < product.attrs.length; i++) {
			if (product.attrs[i][0] == key) {
				product.attrs[i][2] = true;
				return product.attrs[i][1];
			}
		}
		return false;
	}

	window.scrollTo(0, document.body.scrollHeight);
	// start to fill
	// first name and three keywords
	$('#productName').val(product.name);
	// attrs needs to fill
	var attrs = [];
	// attr's key
	$('.attr-title').map(function() {
		attrs.push($(this).html());
	});
	// attrs's value
	var values = $('#productAttribute').find('.ui-form-control');
	// walk through it pair by pair
	attrs.forEach(function(attr_name, key_index) {
		// get attr value from product's attr list by the key
		var attr_val = product.get_attr_val(attr_name);
		// first rule out the attr we don't care
		if (attr_name == 'Place of Origin') {
			$('[name=contryValue]').val('CN-China (Mainland)');
			return;
		}
		// start to fill if you get attr value
		if (attr_val !== false) {
			fill_attr(values[key_index], attr_val);
		} else {
			mark_empty_attr(values[key_index]);
		}
	});
	// loop through all attrs to finish the unfilled attr
	product.attrs.forEach(function(attr) {
		if (!attr[2]) {
			add_more_attr(attr[0], attr[1]);
		}
	});

	// trade information
	$('#minOrderQuantity').val(product.min_order_quantity);
	$('#minOrderUnit').val(product.min_order_unit);
	$('#moneyType').val(product.money_type);
	$('#priceRangeMin').val(product.price_range_min);
	$('#priceRangeMax').val(product.price_range_max);
	$('#priceUnit').val(product.price_unit);
	$('#port').val(product.port);
	check_payment_box(product.payment_terms);
	$('#supplyQuantity').val(product.supply_quantity);
	$('#supplyUnit').val(product.supply_unit);
	$('#supplyPeriod').val(product.supply_period);
	$('#consignmentTerm').val(product.consignment_term);
	$('#packagingDesc').val(product.packaging_desc);
}

function auto_fill_rich_text(product) {
	var rich_f = function(content) {
		if (content.constructor === Array) {
			content = content.join('');
		}
		tinyMCE.activeEditor.setContent(content);
	}
	var rich_code = '(' + rich_f.toString() + ')(' + JSON.stringify(product.rich_text) + ')';
	var script = document.createElement('script');
	script.textContent = rich_code;
	setTimeout(function() {
		(document.head || document.documentElement).appendChild(script);
		script.parentNode.removeChild(script);
	}, 2000);
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	if (request.action == 'set_product') {
		product = request.product;

		$('#productName').after('<button id="auto_fill" type="button" class="ui-button ui-button-normal ui-button-big">自动填写</button>');

		$('#auto_fill').click(function() {
			auto_fill_product(product);
			fill_keywords(product);
			auto_fill_rich_text(product);
		});
	}

	// set the category
	if (request.action == 'set_category') {
		$('#search-keyword').val(request.category[request.category.length - 1]);
		$('button[type=submit]').click();
	}

});