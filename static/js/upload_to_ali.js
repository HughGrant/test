django.jQuery(function($) {
    $('.ali_u').click(function() {
        var id = $(this).attr('id');
        var model = $(this).attr('model');
        var url = location.origin + '/products/capture/';
        var data = {id: id, model: model}
        $.get(url, data).done(function(data) {
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
    });

    btn = '<button id="show_tiny" type="button">显示编辑</button>';
    $('.form-row.field-basic>div').append(btn);

    $('#show_tiny').click(function() {
        init_tinymce_all();
    });
});

function init_tinymce_all(selector) {
    tinymce.init({
        selector: ".vLargeTextField",
        menubar: false,
        statusbar: false,
        toolbar1: "code undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent",
        plugins: ["code"],
        height: 400
    });
}