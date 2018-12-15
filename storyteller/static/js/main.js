(function(){

    $(window).scroll(function () {
        var scroll = $(this).scrollTop();
        if(scroll > 3){
            $('.navbar').addClass('bg-light').children('div >div > ul.navbar-nav button').removeClass('btn-wh');
        }
        else if(scroll == 0){
            $('.navbar').removeClass('bg-light');
        }
    });
})();