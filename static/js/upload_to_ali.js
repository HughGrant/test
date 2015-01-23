django.jQuery(function($) {
    $('.ali_upload').click(function() {
        var pid = $(this).attr('id');
        var url = location.origin + '/products/capture/';
        $.get(url, {id:pid}).done(function(data) {
            if (data.status) {
                // var content = JSON.stringify(data.data.rich_text);
                // var rich_f = function(content) {
                //     console.log(content);
                // }
                // var rich_code = '(' + rich_f.toString() + ')(' + content + ')';
                // var script = document.createElement('script')
                // script.textContent = rich_code
                // setTimeout(function(){
                //     (document.head || document.documentElement).appendChild(script)
                //     script.parentNode.removeChild(script)
                // }, 1000)
                var evt = new CustomEvent('upload_product', {'detail': data.data})
                document.dispatchEvent(evt);
            } else {
                alert(data.message);
            }
        }).fail(function() {
            alert(data.message);
        });
        return false;
    })
})