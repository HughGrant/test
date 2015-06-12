// invoked at command_plaste.js
var capture_product = function(product) {
    product.rich_text = [];
    data = {
        'json': JSON.stringify(product)
    };

    $.post(CAPTURE_PRODUCT_URL, data).done(function(data) {
        if (data.status) {
            alert('抓取成功');
        } else {
            alert(data.message);
        }
    }).fail(function(data) {
        alert('出错了');
    });
}

function get_inner_text(css_selector, default_str) {
    var attr = $(css_selector);
    if (attr.length) {
        return $.trim(attr[0].innerText);
    }
    return default_str || '';
}

function scratch() {
    var product = {}
    product.name = get_product_name();

    product.category = array_trim($('.ui-breadcrumb').attr('content').split('>'))

    product.unkown_category_id = $('.num').html().replace(/[()]/g, '');
    // main images src
    product.photos = get_main_pictures()

    product.attrs = []
    keys = $('.J-name')
    values = $('.J-value')
    for (var i = 0; i < keys.length; i++) {
        product.attrs.push([keys[i].innerText.replace(/:/g, ''), $.trim(values[i].innerText)])
    }

    product.consignment_term = get_inner_text('td:contains("Delivery Detail:") + td')
    product.packaging_desc = get_inner_text('td:contains("Packaging Details:") + td')

    // Example on page: "US $ 130 - 165 / Set | Get Latest Price"
    var priceInfo = $('th:contains("FOB Price:") + td')[0]
    if (priceInfo.childElementCount != 4) {
        // means it only got a <a> contains "Get Latest Price"
        product.price_range_min = 0;
        product.price_range_max = 0;
        // in preset.py money_type USD is 1
        product.money_type = 1;
        product.price_unit = 20;
    } else {
        var nt = $.trim(priceInfo.childNodes[5].textContent).split(' ')[1]
        product.price_unit = unitType[nt]
        // currency short name: such as US
        var csn = priceInfo.childNodes[1].textContent.split(' ')[0]
        product.money_type = moneyType[csn].value
        product.price_range_min = parseInt(priceInfo.childNodes[2].textContent)
        product.price_range_max = parseInt(priceInfo.childNodes[4].textContent)
    }

    var MOQ = $('th:contains("Min.Order Quantity:") + td')[0].innerText
    MOQ = MOQ.split(' ')
    product.min_order_quantity = parseInt(MOQ[0])
    product.min_order_unit = unitType[MOQ[1]]


    product.port = get_inner_text('th:contains("Port:") + td', 'NingBo');


    var pm = $('th:contains("Payment Terms:") + td')[0].innerText
    product.payment_terms = array_trim(pm.split(','))

    var supply = $('th:contains("Supply Ability:") + td')[0].innerText
    supply = supply.split(' ')

    product.supply_unit = unitType[supply[1]]
    product.supply_quantity = parseInt(supply[0])
    product.supply_period = supply[supply.length - 1]

    var rich = get_rich_text();
    product.rich_text = rich.txt.join('');

    if (rich.imgs.length > 0) {
        for (var i = rich.imgs.length - 1; i >= 0; i--) {
            product.photos.push(rich.imgs[i]);
        }
    }
    product.photos.reverse();
    return product;
}

function get_product_name() {
    return $('.title.fn')[0].innerText;
}

function get_main_pictures() {
    var mp = [];
    $('.inav.util-clearfix img').each(function() {
        mp.push($(this).attr('src'));
    });
    return mp;
}

function get_rich_text() {
    // this function return a dict
    var div = $('#J-rich-text-description');
    var eles = div.find('> p, > table, > ul');
    rich = {};
    rich.txt = [];
    rich.imgs = [];
    for (var i = 0; i < eles.length; i++) {
        var img = $(eles[i]).find('img');
        if (img.length == 0) {
            var html = eles[i].outerHTML;
            rich.txt.push(html);
        }
    }

    var imgs = div.find('noscript');
    for (var i = imgs.length - 1; i >= 0; i--) {
        var src = $(imgs[i].innerText).attr('src');
        rich.imgs.push(src);
    }
    return rich;
}

function array_trim(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i] = $.trim(arr[i]);
    }
    return arr;
}