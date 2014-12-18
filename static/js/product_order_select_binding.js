django.jQuery(function($) {
    $("select[name*=product]").bind('change', function() {
        var select = $(this);
        if ($.trim(select.val()) == '') { return false; }
        var url ='/admin/buss/order/products_basic/' + select.val() + '/';
        $.get(url).done(function(data) {
            var index = select.attr('name').split('-')[1];
            var quantity = ['productorder_set', index, 'quantity'].join('-');
            var cost = ['productorder_set', index, 'cost'].join('-');
            quantity = $('input[name="' + quantity + '"]');
            cost = $('input[name="' + cost + '"]');
            if (parseInt(quantity.val()) == 0) {
                quantity.val(1);
                cost.val(data.cost);
            } else {
                cost.val(data.cost * quantity.val())
            }
            update_total_cost();
        });
    });

    $("input[name*=quantity]").bind('change', function() {
        var input = $(this);
        var index = input.attr('name').split('-')[1];
        var cost = ['productorder_set', index, 'cost'].join('-');
        cost = $('input[name="' + cost + '"]');
        var new_cost = input.val() * cost.val();
        cost.val(new_cost);
        update_total_cost();
    });

    
    $(".field-cost>input[name*=cost]").bind('change', function() {
        update_total_cost();
    });

    function update_total_cost() {
        var count = 0;
        $(".field-cost>input[name*=cost]").map(function() {
            count += parseInt($(this).val());
        });
        $("#id_total_cost").val(count)
    }
});