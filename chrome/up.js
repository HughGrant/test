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
	var input = '<input value="' + value + '" id="" name="' + input_name + '" type="text" class="attr-inline type-other TAG:main" maxlength="70" style="width: 180px;">';
	return input;
}

function select_by_text(elem, text) {
	var name = elem.attr('name');
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
		$(elem).after(input);
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
	elem = $(elem)
	var defaults = elem.find('span').map(function() {
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
		var other = elem.find('input:eq(0)');
		var name = other.attr('name');
		var input = create_other_input(name, left.join(', '));
		other.prop('checked', true);
		var xxx = elem.find('label:eq(' + (defaults.length - 1) + ')');
		xxx.after(input);
	}
}

function fill_attr(elem, val) {
	var a = $(elem);

	if (a.find('input[type=text]').size() > 0) {
		a.find('input').val(val);
	} else if (a.find('select').size() > 0) {
		select_by_text(a.find('select'), val);
	} else if (a.find('input[type=checkbox]').size() > 0) {
		check_box(elem, val.split(','));
	}
}

function mark_empty_attr(elem) {
	// could be one of the following
	$(elem).find('input[type=text]').css('border', '2px solid red');
	$(elem).find('select').css('border', '2px solid red');
	$(elem).find('input[type=checkbox]').css('border', '2px solid red');
}

function fill_keywords(search_keyword) {
    var url =  KW_URL + '?count=3&name=' + search_keyword
    $.get(url).done(function(data) {
        // need to login to continue
        if (!data.status && data.message) {
            alert(data.message);
            return false;
        }

        if (data.status) {
            var key2 = $('#keywords2'),
                key3 = $('#keywords3'),
                key1 = $('#productKeyword');
            
            key1.val(data.result.shift());
            key2.val(data.result.shift());
            key3.val(data.result.shift());
        } else {
            var f = confirm('关键字不足, 否现在去采集?');
            if (f) {
                collect_keywords(search_keyword);
            }
        }

    }).fail(function(data) {
        alert(data.message);
    });
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	if (request.action == 'set_product') {
		product = request.product;

		$('#productName').after('<button id="auto_fill" type="button" class="ui-button ui-button-normal ui-button-big">自动填写</button>');
		$('#browser').after('<button id="download_imgs" type="button" class="ui-button ui-button-normal ui-button-small" style="margin-left:5px;">下载原文图片</button>');
		$('#browser').after('<button id="check_imgs" type="button" class="ui-button ui-button-normal ui-button-small" style="margin-left:5px;">查看原文图片</button>');

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
			// find out what lang that this page is in
			var is_en = $('.ui-header-lan-display-text').html() == 'English';
			if (!is_en) {
				alert('请先把页面语言设置为英文');
				return false;
			}
			// set up product object
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
			// first name and primary product keyword
			$('#productName').val(product.name);
			if ($.trim(product.keyword) != '') {
                $('#addMoreKeywords').click(function() {
                    setTimeout(function() {
                        fill_keywords(product.keyword);
                    }, 1000);
                });
			};
			// attrs needs to fill
			var attrs = [];
			$('.attr-title').map(function() {
				attrs.push($(this).html().replace(':', ''));
			});
			// attrs's value
			var values = $('.attribute-table-td');

			attrs.forEach(function(attr_name, index) {
				var attr_val = product.get_attr_val(attr_name);
				if (attr_name == 'Place of Origin') {
					$('[name=contryValue]').val('CN-China (Mainland)');
					return;
				}
				// start to fill
				if (attr_val !== false) {
					fill_attr(values[index], attr_val);
				} else {
					mark_empty_attr(values[index]);
					console.log("should have this standarded attr:" + attr_name);
				}
			});
			// loop through all attrs to finish the unfilled attr
			product.attrs.forEach(function(attr) {
				if (!attr[2]) {
					add_more_attr(attr[0], attr[1]);
				}
			});

			// trade information
			$('#minOrderQuantity').val(product.min_order_quantity)
			$('#minOrderUnit').val(product.min_order_unit)
			$('#moneyType').val(product.money_type)
			$('#priceRangeMin').val(product.price_range_min)
			$('#priceRangeMax').val(product.price_range_max)
			$('#priceUnit').val(product.price_unit)
			$('#port').val(product.port)
			check_payment_box(product.payment_terms)
			$('#supplyQuantity').val(product.supply_quantity)
			$('#supplyUnit').val(product.supply_unit)
			$('#supplyPeriod').val(product.supply_period)
			$('#consignmentTerm').val(product.consignment_term)
			$('#packagingDesc').val(product.packaging_desc)
			// rich text
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
			}, 1000);
		});
	}

	// set the category
	if (request.action == 'set_category') {
		$('#search-keyword').val(request.category[request.category.length - 1])
		$('button[type=submit]').click()
	}

});