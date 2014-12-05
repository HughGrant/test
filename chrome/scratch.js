$(function(){
  $('.buttons').append('<div class="item"><a id="scratch_trigger" class="ui-button ui-button-normal ui-button-large atm dot-app-pd atmonline">复制产品</a></div>')
  $('#scratch_trigger').click(function() {
    product = scratch()
    // model_insert('products', product, '复制产品成功', '出错了')
    product_upload(product)
  })
})

function scratch() {
  var product = {}
  product.name = $('h1.fn')[0].innerText

  product.category = array_trim($('.ui-breadcrumb').attr('content').split('>'))

  product.photos = []
  product.photos.push($('.photo.pic.J-pic')[0].src)

  product.attrs = []
  keys = $('.J-name')
  values = $('.J-value')
  for(var i = 0; i < keys.length; i++) {
    product.attrs.push([keys[i].innerText.replace(':', ''), $.trim(values[i].innerText)])
  }

  product.consignment_term = $('td:contains("Packaging Detail:") + td')[0].innerText
  product.packaging_desc = $('td:contains("Delivery Detail:") + td')[0].innerText

  product.summary = $('p.description')[0].innerText

  var priceInfo = $('th:contains("FOB Price:") + td')[0].innerText
  if (priceInfo == "Get Latest Price") {
    product.price_range_min = 0
    product.price_range_max = 0
    product.money_type = 'USD'
    product.price_unit = 20
  } else {
    priceInfo = priceInfo.split('/')
    var unitInfo = $.trim(priceInfo[1]).split(' ')[0]
    product.price_unit = unitType[unitInfo]
    var moneyInfo = priceInfo[0].split(' ')
    product.money_type = moneyType[moneyInfo[0]].value
    product.price_range_max = parseInt(moneyInfo[3])
    product.price_range_min = parseInt(moneyInfo[1].substring(1))
  }

  var MOQ = $('th:contains("Min.Order Quantity:") + td')[0].innerText
  MOQ = MOQ.split(' ')
  product.min_order_quantity = parseInt(MOQ[0])
  product.min_order_unit = unitType[MOQ[1]]
  
  
  var port = $('th:contains("Port:") + td')[0].innerText
  product.port = $.trim(port)

  var pm = $('th:contains("Payment Terms:") + td')[0].innerText
  product.payment_method = array_trim(pm.split(','))

  var supply = $('th:contains("Supply Ability:") + td')[0].innerText
  supply = supply.split(' ')

  product.supply_unit = unitType[supply[1]]
  product.supply_quantity = parseInt(supply[0])
  product.supply_period = supply[supply.length - 1]
  
  var rich = get_rich_text() 
  product.rich_text = rich.txt

  if (rich.imgs.length > 0) {
    for (var i = rich.imgs.length - 1; i >= 0; i--) {
      product.photos.push(rich.imgs[i])
    }
  }
  return product
}

function get_rich_text() {
  var div = $('#J-rich-text-description')
  var eles = div.find('> p, > table, > ul')
  rich = {}
  rich.txt = []
  rich.imgs = []
  for(var i = 0; i < eles.length; i++) {
    var img = $(eles[i]).find('img')
    if (img.length == 0) {
      var html = eles[i].outerHTML
      rich.txt.push(html)
    }
  }

  var imgs = div.find('noscript')
  for (var i = imgs.length - 1; i >= 0; i--) {
    var src = $(imgs[i].innerText).attr('src')
    rich.imgs.push(src)
  }
    // } else {
    //   for (var j = img.length - 1; j >= 0; j--) {
    //     rich.imgs.push(img[j].src)
    //   }
    // } 
  return rich
}

function array_trim(arr) {
  for(var i = 0; i < arr.length; i++) {
    arr[i] = $.trim(arr[i])
  }
  return arr
}
