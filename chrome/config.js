var DOMAIN = 'http://localhost:8000/'
var ADMIN_URL = DOMAIN + 'admin/'
var LOGIN_URL = DOMAIN + 'chrome_login/'
var LOGOUT_URL = DOMAIN + 'logout/'
var KW_URL = DOMAIN + 'products/keyword/'
var SEARCH_HOT_KEYWORD_URL = 'http://hz.my.data.alibaba.com/industry/keywords.htm'
var UPLOAD_PRODUCT_URL = 'http://hz.productposting.alibaba.com/product/posting.htm'

var get_delivery_cost = function(countryId, weight) {
  chrome.runtime.sendMessage({action:'delivery_cost', countryId:countryId, weight:weight})
}

var model_insert = function(model_name, data, success_msg, error_msg) {
  $.ajax({
    url: DOMAIN + model_name,
    data: JSON.stringify(data),
    type: 'POST',
    success: function(data) {
      alert(success_msg)
    },
    error: function(data) {
      alert(error_msg)
    }
  })
}

var setup_keywords_ui = function() {
  $('#productKeyword').after('<button id="get_keywords" type="button" class="ui-button ui-button-normal ui-button-big">更多关键字</button>')
  $('#keywords3').after('<button id="clear_keywords" type="button" class="ui-button ui-button-normal ui-button-big">清除</button>')
  
  
  $('#get_keywords').click(get_keywords)
  $('#clear_keywords').click(function() {
    $('#keywords2').val('')
    $('#keywords3').val('')
  })
}

var set_keywords = function(data) {
  var key2 = $('#keywords2'),
      key3 = $('#keywords3');
  
  if ($.trim(key2.val()) == '') { key2.val(data.result.shift()) }
  if ($.trim(key3.val()) == '') { key3.val(data.result.shift()) }
}

var open_url = function(url) {
  chrome.runtime.sendMessage({action: 'open_url', url: url})
}

var download_url = function(url, filename) {
  chrome.runtime.sendMessage({
    action: 'download_url',
    url: url,
    filename: filename
  });
}

var get_keywords = function() {
  var mk = $('#productKeyword');
  if ($.trim(mk.val()) == '') {
    mk.css('border', '2px solid red');
    return false;
  }

  var tmp = mk.val().split(' ');
  var clean_name = [];
  tmp.forEach(function(i){
    if (i != '') { clean_name.push(i)};
  });
  mk.val(clean_name.join(' '));

  var name = $.trim(mk.val()),
      key2 = $.trim($('#keywords2').val()),
      key3 = $.trim($('#keywords3').val()),
      count = 0;

  if (key2 == '') { count++ }
  if (key3 == '') { count++ }
  if (count == 0) { return false }

  var url =  KW_URL + '?count=' + count + '&name=' + name
  $.get(url).done(function(data) {
    if (data.status) {
      set_keywords(data);
    } else {
      var f = confirm('关键字不足, 否现在去采集?');
      if (f) {
        collect_keywords(mk.val());
      }
    }
  }).fail(function(data) {
    alert(data.message);
  });
}

var collect_keywords = function(name) {
  chrome.runtime.sendMessage({action: 'collect_keywords', name: name});
}

var product_upload = function(product) {
  chrome.runtime.sendMessage({action: 'upload_product', product: product});
}

var check_img = function(url) {
  open_url(url);
}


var ATTR = [
  ["售后服务体系", "After-sales Service Provided", "select"],
  ["保修期", "Warranty", "input"],
  ["认证", "Certification", "input"],
  ["重量", "Weight", "input"],
  ["尺寸(长×宽×高)", "Dimension(L*W*H)", "input"],
  ["功率(瓦)", "Power(W)", "input"],
  ["功率", "Power", "input"],
  ["动力类型", "Driven Type", "select"],
  ["自动化程度", "Automatic Grade", "select"],
  ["包装材料", "Packaging Material", "check"],
  ["包装类型", "Packaging Type", "check"],
  ["电压", "Voltage", "input"],
  ["型号", "Model Number", "input"],
  ["品牌", "Brand Name", "input"],
  ["原产地", "Place of Origin", "select"],
  ["编程控制", "Computerized", "select"],
  ["箱包材质", "Material", "select"],
  ["材质", "Material", "select"],
  ["箱包类型", "Bag Type", "select"],
  ["机器类型", "Machine Type", "select"],
  ["状态", "Condition", "select"],
  ["新旧程度", "Condition", "select"],
  ["类型", "Type", "select"],
  ["种类", "Type", "select"],
  ["应用", "Application", "check"],
  ["最大压片直径", "Max. Tablet Diameter(mm)", "input"],
  ["最大压片厚度", "Max. Tablet Thickness(mm)", "input"],
  ["最大压力", "Max. Pressure(KN)", "input"],
  ["生产率", "Production Capacity", "input"],
]

var moneyType = {
  US: {value: 1, text: 'USD'},
  CH: {value: 2, text: 'RMB'},
  EU: {value: 3, text: 'EUR'},
  OT: {value: 4, text: 'Other'},
  GB: {value: 5, text: 'GBP'},
  JP: {value: 6, text: 'JPY'},
  AU: {value: 7, text: 'AUD'},
  CA: {value: 8, text: 'CAD'},
  CF: {value: 9, text: 'CHF'},
  NT: {value: 11, text: 'NTD'},
  HK: {value: 12, text: 'HKD'},
  NZ: {value: 13, text: 'NZD'},
}

var unitType = {
  'Acre/Acres':                           26,
  'Ampere/Amperes':                       27,
  'Bag/Bags':                             1,
  'Barrel/Barrels':                       19,
  'Blade/Blades':                         91,
  'Box/Boxes':                            28,
  'Bushel/Bushels':                       18,
  'Carat/Carats':                         90,
  'Carton/Cartons':                       29,
  'Case/Cases':                           30,
  'Centimeter/Centimeters':               31,
  'Chain/Chains':                         32,
  'Combo/Combos':                         92,
  'Cubic Centimeter/Cubic Centimeters':   33,
  'Cubic Foot/Cubic Feet':                34,
  'Cubic Inch/Cubic Inches':              35,
  'Cubic Meter/Cubic Meters':             13,
  'Cubic Yard/Cubic Yards':               36,
  'Degrees Celsius':                      37,
  'Degrees Fahrenheit':                   38,
  'Dozen/Dozens':                         14,
  'Dram/Drams':                           39,
  'Fluid Ounce/Fluid Ounces':             40,
  'Foot/Feet':                            41,
  'Forty-Foot Container':                 88,
  'Furlong/Furlongs':                     42,
  'Gallon/Gallons':                       15,
  'Gill/Gills':                           43,
  'Grain/Grains':                         44,
  'Gram/Grams':                           17,
  'Gross':                                87,
  'Hectare/Hectares':                     45,
  'Hertz':                                46,
  'Inch/Inches':                          47,
  'Kiloampere/Kiloamperes':               48,
  'Kilogram/Kilograms':                   16,
  'Kilohertz':                            49,
  'Kilometer/Kilometers':                 10,
  'Kiloohm/Kiloohms':                     50,
  'Kilovolt/Kilovolts':                   51,
  'Kilowatt/Kilowatts':                   52,
  'Liter/Liters':                         22,
  'Long Ton/Long Tons':                   9,
  'Megahertz':                            53,
  'Meter/Meters':                         8,
  'Metric Ton/Metric Tons':               7,
  'Mile/Miles':                           54,
  'Milliampere/Milliamperes':             55,
  'Milligram/Milligrams':                 24,
  'Millihertz':                           56,
  'Milliliter/Milliliters':               57,
  'Millimeter/Millimeters':               58,
  'Milliohm/Milliohms':                   59,
  'Millivolt/Millivolts':                 60,
  'Milliwatt/Milliwatts':                 61,
  'Nautical Mile/Nautical Miles':         62,
  'Ohm/Ohms':                             63,
  'Ounce/Ounces':                         6,
  'Pack/Packs':                           21,
  'Pair/Pairs':                           5,
  'Pallet/Pallets':                       86,
  'Parcel/Parcels':                       64,
  'Perch/Perches':                        65,
  'Piece/Pieces':                         4,
  'Pint/Pints':                           66,
  'Plant/Plants':                         85,
  'Pole/Poles':                           67,
  'Pound/Pounds':                         3,
  'Quart/Quarts':                         68,
  'Quarter/Quarters':                     69,
  'Rod/Rods':                             70,
  'Roll/Rolls':                           71,
  'Set/Sets':                             20,
  'Sheet/Sheets':                         89,
  'Short Ton/Short Tons':                 2,
  'Square Centimeter/Square Centimeters': 72,
  'Square Foot/Square Feet':              73,
  'Square Inch/Square Inches':            74,
  'Square Meter/Square Meters':           12,
  'Square Mile/Square Miles':             75,
  'Square Yard/Square Yards':             76,
  'Stone/Stones':                         77,
  'Strand/Strands':                       84,
  'Ton/Tons':                             11,
  'Tonne/Tonnes':                         78,
  'Tray/Trays':                           79,
  'Twenty-Foot Container':                83,
  'Unit/Units':                           25,
  'Volt/Volts':                           80,
  'Watt/Watts':                           81,
  'Wp':                                   82,
  'Yard/Yards':                           23,
  'Acre':                                 26,
  'Ampere':                               27,
  'Bag':                                  1,
  'Barrel':                               19,
  'Blade':                                91,
  'Box':                                  28,
  'Bushel':                               18,
  'Carat':                                90,
  'Carton':                               29,
  'Case':                                 30,
  'Centimeter':                           31,
  'Chain':                                32,
  'Combo':                                92,
  'Cubic Centimeter':                     33,
  'Cubic Foot':                           34,
  'Cubic Inch':                           35,
  'Cubic Meter':                          13,
  'Cubic Yard':                           36,
  'Degrees Celsius':                      37,
  'Degrees Fahrenheit':                   38,
  'Dozen':                                14,
  'Dram':                                 39,
  'Fluid Ounce':                          40,
  'Foot':                                 41,
  'Forty-Foot Container':                 88,
  'Furlong':                              42,
  'Gallon':                               15,
  'Gill':                                 43,
  'Grain':                                44,
  'Gram':                                 17,
  'Gross':                                87,
  'Hectare':                              45,
  'Hertz':                                46,
  'Inch':                                 47,
  'Kiloampere':                           48,
  'Kilogram':                             16,
  'Kilohertz':                            49,
  'Kilometer':                            10,
  'Kiloohm':                              50,
  'Kilovolt':                             51,
  'Kilowatt':                             52,
  'Liter':                                22,
  'Long Ton':                             9,
  'Megahertz':                            53,
  'Meter':                                8,
  'Metric Ton':                           7,
  'Mile':                                 54,
  'Milliampere':                          55,
  'Milligram':                            24,
  'Millihertz':                           56,
  'Milliliter':                           57,
  'Millimeter':                           58,
  'Milliohm':                             59,
  'Millivolt':                            60,
  'Milliwatt':                            61,
  'Nautical Mile':                        62,
  'Ohm':                                  63,
  'Ounce':                                6,
  'Pack':                                 21,
  'Pair':                                 5,
  'Pallet':                               86,
  'Parcel':                               64,
  'Perch':                                65,
  'Piece':                                4,
  'Pint':                                 66,
  'Plant':                                85,
  'Pole':                                 67,
  'Pound':                                3,
  'Quart':                                68,
  'Quarter':                              69,
  'Rod':                                  70,
  'Roll':                                 71,
  'Set':                                  20,
  'Sheet':                                89,
  'Short Ton':                            2,
  'Square Centimeter':                    72,
  'Square Foot':                          73,
  'Square Inch':                          74,
  'Square Meter':                         12,
  'Square Mile':                          75,
  'Square Yard':                          76,
  'Stone':                                77,
  'Strand':                               84,
  'Ton':                                  11,
  'Tonne':                                78,
  'Tray':                                 79,
  'Twenty-Foot Container':                83,
  'Unit':                                 25,
  'Volt':                                 80,
  'Watt':                                 81,
  'Wp':                                   82,
  'Yard':                                 23,
}

var countryInfo = [
  [84,"美国","United States","US"],
  [85,"澳大利亚","Australia","AU"],
  [80,"英国","United Kingdom","GB"],
  [83,"加拿大","Canada","CA"],
  [165,"委内瑞拉","Venezuela","VE"],
  [166,"美属萨摩亚","American Samoa","AS"],
  [167,"库克群岛","Cook Is.","CK"],
  [168,"斐济","Fiji","FJ"],
  [169,"关岛(美)","Guam","GU"],
  [170,"马里亚纳群岛","Mariana","MP"],
  [171,"瑙鲁","Nauru","NR"],
  [172,"新喀里多尼亚群岛(法)","New Caledonia","NC"],
  [173,"诺福克","Norfolk","NF"],
  [174,"巴布亚新几内亚","Papua New Guinea","PG"],
  [175,"所罗门群岛","Solomon","SB"],
  [176,"汤加","Tonga","TO"],
  [177,"瓦努阿图","VANUATU","VU"],
  [178,"图瓦卢","Tuvalu","TV"],
  [179,"阿根廷","Argentina","AR"],
  [180,"玻利维亚","Bolivia","BO"],
  [181,"巴西","Brazil","BR"],
  [182,"智利","Chile","CL"],
  [183,"哥伦比亚","Colombia","CO"],
  [184,"厄瓜多尔","Ecuador","EC"],
  [185,"圭亚那(英国)","Guyana","GY"],
  [186,"巴拉圭","Paraguay","PY"],
  [187,"秘鲁","Peru","PE"],
  [188,"乌拉圭","Uruguay","UY"],
  [189,"亚美尼亚","Armenia","AM"],
  [190,"白俄罗斯","Belarus","BY"],
  [191,"波斯尼亚和黑塞哥维那","Bosnia Herzegovina","BA"],
  [193,"东帝汶","East Timor","TP"],
  [194,"厄立特里亚","Eritrea","ER"],
  [195,"格鲁吉亚","Georgia","GE"],
  [196,"吉尔吉斯斯坦","Kirghizia","KG"],
  [197,"科索沃","Kosovo","XO"],
  [198,"列支敦士登","Liechtenstein","LI"],
  [199,"马其顿","Macedonia","MK"],
  [200,"密克罗尼西亚","Micronesia","FM"],
  [201,"密克隆岛","Miquelon",""],
  [202,"黑山共和国","Montenegro","ME"],
  [203,"帕劳群岛","Palau",""],
  [204,"巴勒斯坦","Palestine","BL"],
  [206,"塞尔维亚","Serbia","RS"],
  [207,"斯洛文尼亚","Slovenia","SI"],
  [208,"特立尼达和多巴哥","Trinidad and Tobago","TT"],
  [209,"新西兰属土岛屿","New Zealand other island","XL"],
  [210,"马提尼克","Martinique","MQ"],
  [211,"留尼旺岛","Reunion Island","RE"],
  [212,"维尔京群岛(英属)","Virgin Islands(British)","VG"],
  [213,"维尔京群岛(美)","Vigin Islands(U.S.)","VI"],
  [214,"法属玻利尼西亚","French Polynesia","PF"],
  [216,"萨摩亚","Samoa","WS"],
  [217,"南极洲","Antarctica","AQ"],
  [218,"阿森松","Ascension","XD"],
  [219,"亚速尔","Azores","XH"],
  [220,"巴利阿里群岛","Balearic Islands","XJ"],
  [221,"布维岛","Bouvet Island","BV"],
  [222,"英属印度洋地区","British Indian Ocean Territory","IO"],
  [223,"加那利群岛","Canary Islands","XA"],
  [224,"加罗林群岛","Caroline Islands","XK"],
  [225,"海峡群岛","Channel Islands","XC"],
  [226,"圣诞岛","Christmas Island","CX"],
  [227,"科科斯群岛","Cocos(keeling) Islands","CC"],
  [228,"刚果民主共和国","Congo (DEM. REP. OF)","CD"],
  [229,"科西嘉岛","France-Corsica","XF"],
  [230,"多米尼加共和国","Dominican Republic","DO"],
  [231,"福克兰群岛","Falkland Island (Malvinas)","FK"],
  [232,"法属美特罗波利坦","France Metropolitan","FX"],
  [233,"法属圭亚那","French Guiana","GF"],
  [234,"法属南部领土","French Southern Territories","TF"],
  [235,"加沙及汗尤尼斯","Gaza And Khan Yunis","XE"],
  [236,"几内亚共和国","Guinea Republic","GN"],
  [237,"赫德岛和麦克唐岛","Heard Island And Mcdonald Islands","HM"],
  [238,"基里巴斯","Kiribati","KI"],
  [239,"莱索托","Lesotho","LS"],
  [240,"利比里亚","Liberia","LR"],
  [241,"马德拉","Madeira","XI"],
  [242,"马绍尔群岛","Marshall Islands","MH"],
  [243,"马约特","Mayotte","YT"],
  [244,"缅甸","Myanmar","MM"],
  [245,"荷属安的列斯群岛","Netherlands Antilles","AN"],
  [246,"纽埃","Niue","NU"],
  [247,"圣赫勒拿岛","Saint Helena","SH"],
  [248,"尼维斯岛","Nevis","KN"],
  [249,"圣基茨岛","Saint Kitts","KN"],
  [250,"圣皮埃尔和密克隆群岛","Saint Pierre And Miquelon","PM"],
  [251,"圣文森特","Saint Vincent","VC"],
  [252,"圣多美和普林西","Sao Tome And Principe","ST"],
  [253,"南乔治亚岛和南桑德韦奇岛","South Georgia And The South Sandwich Isl","GS"],
  [254,"北非西班牙属土","Spanish Territories Of N.AFRICA","XG"],
  [255,"斯匹次卑尔根群岛","Spitsbergen(Svalbard)","SJ"],
  [256,"托克劳","Tokelau","TK"],
  [257,"特里斯坦(达库尼亚岛)","Tristan Da Cunha","XB"],
  [258,"特克斯和凯科斯群岛","Turks And Caicos Islands","TC"],
  [259,"美国本土外小岛屿","United States Minor Outlying Islands","UM"],
  [260,"威克岛","Wake Island","XM"],
  [261,"瓦利斯群岛和富图纳群岛","Wallis And Futuna Islands","WF"],
  [262,"西撒哈拉","Western sahara","EH"],
  [263,"塞班岛","Saipan Island",""],
  [264,"泽西岛","Jersey","JE"],
  [265,"塔希提","Tahiti",""],
  [266,"圣马丁岛","ST. Maarten",""],
  [267,"圣巴特勒米岛","ST. Barthelemy",""],
  [268,"伯奈尔","Bonaire",""],
  [269,"库拉索岛","Curacao",""],
  [270,"根西岛","Guernsey",""],
  [271,"圣尤斯特歇斯","ST. Eustatius",""],
  [1,"朝鲜","D.P.R.Korea","KP"],
  [2,"日本","Japan","JP"],
  [3,"哈萨克斯坦","Kazakhstan","KZ"],
  [4,"蒙古","Mongolia","MN"],
  [5,"韩国","Korea","KR"],
  [6,"塔吉克斯坦","Tadzhikistan","TJ"],
  [7,"土库曼斯坦","Turkmenistan","TM"],
  [8,"乌兹别克斯坦","Uzbekistan","UZ"],
  [9,"越南","Viet Nam","VN"],
  [10,"阿富汗","Afghanistan","AF"],
  [11,"阿尔巴尼亚","Albania","AL"],
  [12,"阿塞拜疆","Azerbaijan Republic","AZ"],
  [13,"巴林","Bahrain","BH"],
  [14,"孟加拉国","Bangladesh","BD"],
  [15,"不丹","Bhutan","BT"],
  [16,"文莱","Brunei","BN"],
  [17,"柬埔寨","Cambodia","KH"],
  [18,"中国香港","Hong kong","HK"],
  [19,"印度","India","IN"],
  [20,"印尼","Indonesia","ID"],
  [21,"伊朗","Iran","IR"],
  [22,"伊拉克","Iraq","IQ"],
  [23,"以色列","Israel","IL"],
  [24,"约旦","Jordan","JO"],
  [25,"科威特","Kuwait","KW"],
  [26,"老挝","Laos","LA"],
  [27,"黎巴嫩","Lebanon","LB"],
  [28,"卢森堡","Luxembourg","LU"],
  [29,"澳门","Macao","MO"],
  [30,"马来西亚","Malaysia","MY"],
  [31,"马尔代夫","Maldives","MV"],
  [32,"尼泊尔","Nepal","NP"],
  [33,"阿曼","Oman","OM"],
  [34,"巴基斯坦","Pakistan","PK"],
  [35,"菲律宾","Philippines","PH"],
  [36,"卡塔尔","Qatar","QA"],
  [37,"沙特阿拉伯","Saudi Arabia","SA"],
  [38,"新加坡","Singapore","SG"],
  [39,"斯里兰卡","Sri Lanka","LK"],
  [40,"叙利亚","Syria","SY"],
  [41,"台湾","Taiwan","TW"],
  [42,"泰国","Thailand","TH"],
  [43,"土耳其","Turkey","TR"],
  [44,"阿拉伯联合酋长国","United Arab Emirates","AE"],
  [45,"也门共和国","Yemen","YE"],
  [46,"安道尔共和国","Andorra","AD"],
  [47,"奥地利","Austria","AT"],
  [48,"比利时","Belgium","BE"],
  [49,"保加利亚","Bulgaria","BG"],
  [50,"克罗地亚","Croatia, Republic of","HR"],
  [51,"捷克","Czech Republic","CZ"],
  [52,"丹麦","Denmark","DK"],
  [53,"爱沙尼亚","Estonia","EE"],
  [54,"芬兰","Finland","FI"],
  [55,"法国","France","FR"],
  [56,"德国","Germany","DE"],
  [57,"直布罗陀(英)","Gibraltar","GI"],
  [58,"希腊","Greece","GR"],
  [59,"匈牙利","Hungary","HU"],
  [60,"冰岛","Iceland","IS"],
  [61,"爱尔兰","Ireland","IE"],
  [62,"意大利","Italy","IT"],
  [63,"拉脱维亚","Latvia","LV"],
  [64,"立陶宛","Lithuania","LT"],
  [65,"马耳他","Malta","MT"],
  [66,"摩尔多瓦共和国","Moldova","MD"],
  [67,"摩纳哥","Monaco","MC"],
  [68,"荷兰","Netherlands","NL"],
  [69,"挪威","Norway","NO"],
  [70,"波兰","Poland","PL"],
  [71,"葡萄牙","Portugal","PT"],
  [72,"罗马尼亚","Romania","RO"],
  [73,"俄罗斯","Russia","RU"],
  [74,"圣马力诺","San Marino","SM"],
  [75,"斯洛伐克","Slovakia","SK"],
  [76,"西班牙","Spain","ES"],
  [77,"瑞典","Sweden","SE"],
  [78,"瑞士","Switzerland","CH"],
  [79,"乌克兰","Ukraine","UA"],
  [81,"梵蒂冈","Vatican City","VA"],
  [86,"新西兰","New Zealand","NZ"],
  [87,"塞浦路斯","Cyprus","CY"],
  [88,"阿尔及利亚","Algeria","DZ"],
  [89,"安哥拉","Angola","AO"],
  [90,"阿鲁巴","Aruba","AW"],
  [91,"贝宁","Benin","BJ"],
  [92,"博茨瓦纳","Botswana","BW"],
  [93,"布基纳法索","Burkina Faso","BF"],
  [94,"布隆迪","Burundi","BI"],
  [95,"喀麦隆","Cameroon","CM"],
  [96,"佛得角","Cape Verde Is.","CV"],
  [97,"中非共和国","Central Africa","CF"],
  [98,"乍得","Chadian","TD"],
  [99,"科摩罗","Comoros","KM"],
  [100,"刚果","Congo","CG"],
  [101,"吉布提","Djibouti","DJ"],
  [102,"埃及","Egypt","EG"],
  [103,"赤道几内亚","Equatorial Guinea","GQ"],
  [104,"埃塞俄比亚","Ethiopia","ET"],
  [105,"加蓬","Gabon","GA"],
  [106,"冈比亚","Gambia","GM"],
  [107,"加纳","Ghana","GH"],
  [108,"几内亚比绍","Guinea-Bissau","GW"],
  [109,"肯尼亚","Kenya","KE"],
  [110,"利比亚","Libya","LY"],
  [111,"马达加斯加","Madagascar","MG"],
  [112,"马拉维","Malawi","MW"],
  [113,"马里","Mali","ML"],
  [114,"毛里塔尼亚","Mauritania","MR"],
  [115,"毛里求斯","Mauritius","MU"],
  [116,"摩洛哥","Morocco","MA"],
  [117,"莫桑比克","Mozambique","MZ"],
  [118,"纳米比亚","Namibia","NA"],
  [119,"尼日尔","Niger","NE"],
  [120,"尼日利亚","Nigeria","NG"],
  [121,"卢旺达","Rwanda","RW"],
  [122,"塞内加尔","Senegal","SN"],
  [123,"塞舌尔","Seychelles","SC"],
  [124,"塞拉利昂","Sierra Leone","SL"],
  [125,"索马里","Somalia","SO"],
  [126,"索马里兰","SOMALILAND, REP OF (NORTH SOMALIA)",""],
  [127,"南非","South Africa","ZA"],
  [128,"苏丹","Sudan","SD"],
  [129,"斯威士兰","Swaziland","SZ"],
  [130,"坦桑尼亚","Tanzania","TZ"],
  [131,"多哥","Togo","TG"],
  [132,"突尼斯","Tunisia","TN"],
  [133,"乌干达","Uganda","UG"],
  [134,"扎伊尔","Zaire","ZR"],
  [135,"赞比亚","Zambia","ZM"],
  [136,"津巴布韦","Zimbabwe","ZW"],
  [137,"科特迪瓦","Cote d'Ivoire","CI"],
  [138,"安圭拉岛","Anguilla","AI"],
  [139,"安提瓜和巴布达","Antigua and Barbuda","AG"],
  [140,"伯利兹","Belize","BZ"],
  [141,"多米尼加","Dominica","DM"],
  [142,"萨尔瓦多","El salvador","SV"],
  [143,"法罗群岛","Faroe Islands","FO"],
  [144,"格陵兰岛","Greenland","GL"],
  [145,"波多黎各","Puerto Rico","PR"],
  [146,"圣卢西亚","Saint Lucia","LC"],
  [147,"苏里南","Surinam","SR"],
  [149,"巴巴多斯","Barbados","BB"],
  [150,"开曼群岛(英)","Cayman Islands","KY"],
  [151,"瓜德罗普岛(法)","Guadeloupe","GP"],
  [152,"蒙特塞拉特岛","Montserrat","MS"],
  [153,"巴哈马国","Bahamas","BS"],
  [154,"百慕大群岛(英)","Bermuda","BM"],
  [155,"哥斯达黎加","Costa Rica","CR"],
  [156,"古巴","Cuba","CU"],
  [157,"格林纳达","Grenada","GD"],
  [158,"危地马拉","Guatemala","GT"],
  [159,"海地","Haiti","HT"],
  [160,"洪都拉斯","Honduras","HN"],
  [161,"牙买加","Jamaica","JM"],
  [162,"墨西哥","Mexico","MX"],
  [163,"尼加拉瓜","Nicaragua","NI"],
  [164,"巴拿马","Panama","PA"]
]

function make_python_fixures(ci) {
  var pk = 1
  var code = ''
  for (var i = ci.length - 1; i >= 0; i--) {
    code += '{\n'
    code += '\t"model": "clients.countries",\n'
    code += '\t"pk": ' + pk + ',\n'
    code += '\t"fields": {\n'
      code += '\t\t"ibt_id": "' + ci[i][0] + '",\n'
      code += '\t\t"cn_name": "' + ci[i][1] + '",\n'
      code += '\t\t"en_name": "' + ci[i][2] + '",\n'
      code += '\t\t"code": "' + ci[i][3] + '",\n'
      code += '\t\t"voltage": "",\n'
      code += '\t\t"socket": ""\n'
      code += '\t}\n'
    code += '},\n'
    pk++
  }
  console.log(code)
}

$.fn.serializeObject = function() {
   var o = {}
   var a = this.serializeArray()
   $.each(a, function() {
       if (o[this.name]) {
           if (!o[this.name].push) {
               o[this.name] = [o[this.name]]
           }
           o[this.name].push(this.value || '')
       } else {
           o[this.name] = this.value || ''
       }
   })
   return o
}

// var jq = document.createElement('script');
// jq.src = "//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
// document.getElementsByTagName('head')[0].appendChild(jq);

// function collect(cs){
//   var options = $(cs);
//   var code = '';
//   for(var i = 0; i < options.length; i++) {
//     var v = options[i].value; 
//     var t = options[i].text;
//     code += "'" + t + "'" + ':' + v + ',\n';
//   }
//   console.log(code);
//   return code;
// }
