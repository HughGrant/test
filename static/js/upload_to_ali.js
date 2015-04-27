django.jQuery(function($) {
    $('.ali_upload').click(function() {
        var pid = $(this).attr('id');
        var url = location.origin + '/products/capture/';
        $.get(url, {id:pid}).done(function(data) {
            if (data.status) {
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
    
    tinymce.init({
        selector: "#id_rich_text",
        menubar: false,
        statusbar: false,
        toolbar1: "code undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent",
        plugins: ["code"],
        height: 400
    });
})