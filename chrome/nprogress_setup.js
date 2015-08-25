// NProgress ajax setup
$(document).ajaxStart(function() {
    NProgress.start();
});

$(document).ajaxSuccess(function() {
    NProgress.done();
});

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