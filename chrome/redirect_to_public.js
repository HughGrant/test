$(function() {
	var title = $('h1>span');
    var new_link = '<a href="' + public_view_url() + '">' + title.html() + '</a>';
    title.html(new_link);
});

var public_view_url = function() {
	var info = location.toString().split('?')[0].split('/');
    var pid = info[info.length - 2].split('-')[0];
    var pname = info[info.length - 1].split('.')[0];
    var purl = 'http://www.alibaba.com/product-detail/' + pname + '_' + pid + '.html';
    return purl;
}