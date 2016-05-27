(function($){
$(document).ready(function(){

$('#cssmenu li.active').addClass('open').children('ul').show();
    $('#cssmenu li.has-sub>a').on('click', function(){
        $(this).removeAttr('href');
        var element = $(this).parent('li');
        if (element.hasClass('open')) {
            element.removeClass('open');
            element.find('li').removeClass('open');
            element.find('ul').slideUp(200);
        }
        else {
            element.addClass('open');
            element.children('ul').slideDown(200);
            element.siblings('li').children('ul').slideUp(200);
            element.siblings('li').removeClass('open');
            element.siblings('li').find('li').removeClass('open');
            element.siblings('li').find('ul').slideUp(200);
        }
    });
});
})(jQuery);

     function input(e) {
    var keypass = document.getElementById("keypass");
    keypass.value = keypass.value + e.value;
}
 
    function del() {
    var keypass = document.getElementById("keypass");
    keypass.value = keypass.value.substr(0, keypass.value.length - 1);
}
$("#keypass").click(function(){
    $("#virtualkey").toggle(1000);
});