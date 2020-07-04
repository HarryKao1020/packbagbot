$(function(){
    var isOpened=true;
    //-------------------------------------
    $('.Sights').mouseenter(function(){
        $(this).stop().animate({top:-10}, {duration:500, easing:'easeOutBounce'});
    });

    $('.Sights').mouseleave(function(){
        $(this).stop().animate({top:0}, {duration:50});
    });
});
