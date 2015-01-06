var product = null

function get_key(name, is_en) {
	for (var i = 0; i < ATTR.length; i++) {
		var kw = {val:ATTR[i][1], way:ATTR[i][2]}
		if (is_en && ATTR[i][1] == name) {
			return kw 
		} else {
			if (ATTR[i][0] == name) {
					return kw
			}
		}
	}

	return false
}

function get_attr_pos(attrs, key) {
	for (var i = 0; i < attrs.length; i++) {
		if (attrs[i][0] == key) {
			return i
		}
	}

	return false
}

function create_attr(key, value) {
	var cai = $('.custom-attr-item').last()
	cai.find('input').first().val(key)
	cai.find('input').last().val(value)
	$('#copyActionButton').click()
}

function select_by_val(elem, val) {
	var name = elem.attr('name')
	$('[name=' + name + ']').val(val)
}

function create_other_input(name, value) {
	var input_name = 'otherAttrContext' + name.replace('sysAttrValueIdAndValue','')
	var input = '<input value="' + value + '" id="" name="' + input_name + '" type="text" class="attr-inline type-other TAG:main" maxlength="70" style="width: 180px;">'
	return input
}

function select_by_text(elem, text) {
	var name = elem.attr('name')
	var option = $('[name=' + name + '] option').filter(function() { 
	    return ($(this).text() == text)
	})
	if (option.length) {
		option.prop('selected', true)
	} else {
		$('[name=' + name + '] option').filter(function() { 
	    return ($(this).text() == 'Other')
		}).prop('selected', true)
		var input = create_other_input(name, text)
		$(elem).after(input)
	}
}

function check_payment_box(values) {
	values.map(function(v) {
		var v = $.trim(v)
		var input = $('input[value="' + v + '"]')
		if (input) {
			input.prop('checked', true)
		} else {
			$('#paymentMethodOther').prop('checked', true)
			var pm = $('#paymentMethodOtherDesc')
			var pre = pm.val()
			var now = pre + ',' + 'v'
			pm.val(now)
		}
	})
}

function check_box(elem, values) {
	elem = $(elem)
	var defaults = elem.find('span').map(function(){
		return $(this).text()
	})

	var left = []
	for (var i = values.length - 1; i >= 0; i--) {
		var find = false
		for (var j = defaults.length - 1; j >= 0; j--) {
			if (values[i] == defaults[j]) {
				find = true
				elem.find('input:eq(' + j + ')').prop('checked', true)
				break
			}
		}
		if (find == false) {
			left.push(values[i])
		}
	}

	if (left.length != 0) {
		var other = elem.find('input:eq(0)')
		var name = other.attr('name')
		var input = create_other_input(name, left.join(', '))
		other.prop('checked', true)
		var xxx = elem.find('label:eq(' + (defaults.length - 1) + ')')
		xxx.after(input)
	}
}

function set_oringal_place() {
	$('[name=contryValue]').val('CN-China (Mainland)')
}

function fill_attr(elem, val, way) {
	if (way == 'check') {
		check_box(elem, val.split(','))
	}

	var op = $(elem).find(way)
	if (op.length == 0) {
		return false
	}

	if (way == 'input') {
		op.val(val)
	}

	if (way == 'select') {
		select_by_text(op, val)
	}
}

function alert_empty_attr(elem, way) {
	$(elem).find(way).css('border', '2px solid red')
}

$(function() {
	setup_keywords_ui()
})

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	if (request.action == 'set_keywords') {
		set_keywords(request.data)
	}

	if (request.action == 'set_product') {
		product = request.product

		$('#productName').after('<button id="auto_fill" type="button" class="ui-button ui-button-normal ui-button-big">填充所有</button>')
		$('#browser').after('<button id="download_imgs" type="button" class="ui-button ui-button-normal ui-button-small" style="margin-left:5px;">下载原文图片</button>')
		$('#browser').after('<button id="check_imgs" type="button" class="ui-button ui-button-normal ui-button-small" style="margin-left:5px;">查看原文图片</button>')

		$('#download_imgs').click(function() {
			var name = $('#productName').val();
			if ($.trim(name) == '') {
				name = product.name;
			}
			for (var i = product.photos.length - 1; i >= 0; i--) {
				download_url(product.photos[i], name + '.jpg');
			}
		});

		$('#check_imgs').click(function() {
			for (var i = product.photos.length - 1; i >= 0; i--) {
				check_img(product.photos[i]);
			}
		})

		$('#auto_fill').click(function() {
			window.scrollTo(0, document.body.scrollHeight)
			// find out what lang that this page is in
			var is_en = $('.ui-header-lan-display-text').html() == 'English'

			$('#productName').val(product.name)
			// alibaba removed this attribute
			// $('#summary').val(product.summary)

			// filling attrs
			var names_clean = []
			$('.attr-title').map(function() {
				names_clean.push($(this).html().replace(':', ''))
			})

			var values = $('.attribute-table-td')
			// inital set for all attrs
			for (var i = product.attrs.length - 1; i >= 0; i--) {
				product.attrs[i][2] = false
			}

			for (var i = 0; i < names_clean.length; i++) {
				// the key here is always English name and way to operate
				var key = get_key(names_clean[i], is_en)
				if (key === false) {
					console.log("fixed attr not defined:" + names_clean[i])
				} else {
					var pos = get_attr_pos(product.attrs, key.val)
					if (pos === false) {
						alert_empty_attr(values[i], key.way)
						console.log("should have this standarded attr:" + names_clean[i])
					} else {
						// rule out some special case
						product.attrs[pos][2] = true
						if (key.val == 'Place of Origin') {
							set_oringal_place()
							continue
						}
						fill_attr(values[i], product.attrs[pos][1], key.way)
					}
				}
			}
			// loop through all attrs to finish the unfilled attr
			for (var i = 0; i < product.attrs.length; i++) {
				if (product.attrs[i][2] === false) {
					create_attr(product.attrs[i][0], product.attrs[i][1])
					product.attrs[i][2] = true
				}
			}

			// trade information
			$('#minOrderQuantity').val(product.min_order_quantity)
			$('#minOrderUnit').val(product.min_order_unit)
			$('#moneyType').val(product.money_type)
			$('#priceRangeMin').val(product.price_range_min)
			$('#priceRangeMax').val(product.price_range_max)
			$('#priceUnit').val(product.price_unit)
			$('#port').val(product.port)
			check_payment_box(product.payment_method)
			$('#supplyQuantity').val(product.supply_quantity)
			$('#supplyUnit').val(product.supply_unit)
			$('#supplyPeriod').val(product.supply_period)
			$('#consignmentTerm').val(product.consignment_term)
			$('#packagingDesc').val(product.packaging_desc)
			// rich text
			var rich_f = function(lines) {
				var content = lines.join('');
				tinyMCE.activeEditor.setContent(content);
			}
			var rich_code = '(' + rich_f.toString() + ')(' + JSON.stringify(product.rich_text) + ')'
			var script = document.createElement('script')
			script.textContent = rich_code
			setTimeout(function(){
				(document.head || document.documentElement).appendChild(script)
				script.parentNode.removeChild(script)
			}, 1000)
		})
	}	

	// set the category
	if (request.action == 'set_category') {
		$('#search-keyword').val(request.category[request.category.length - 1])
		$('button[type=submit]').click()
	}

})
