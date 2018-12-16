(function(){

    $(window).scroll(function () {
        var scroll = $(this).scrollTop();
        if(scroll > 3){
            $('.navbar').addClass('bg-light');            
            $('ul.navbar-nav button').removeClass('btn-wh').removeClass('btn-outline-info').addClass('btn-info');
            $('a.lnav').removeClass('wclr');
        }
        else if(scroll == 0){
            $('.navbar').removeClass('bg-light');
            $('ul.navbar-nav button').removeClass('btn-info').addClass('btn-wh').addClass('btn-outline-info');
            $('a.lnav').addClass('wclr');
        }
    });
}());