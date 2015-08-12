var btn_html = '<li class="add-favorite-li"><a id="go_to_public" class="add-favorite ba-item" id="add-favorite-text"><span class="ba-item-text">前往展示页</span></a></li>';

$(function() {
    $('.add-favorite-li').after(btn_html);
    var purl = goto_public();
    $('#go_to_public').attr('href', purl);
});

var goto_public = function() {
	var info = location.toString().split('?')[0].split('/');
    var pid = info[info.length - 2].split('-')[0];
    var pname = info[info.length - 1].split('.')[0];
    var purl = 'http://www.alibaba.com/product-detail/' + pname + '_' + pid + '.html';
    return purl;
}