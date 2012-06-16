/***************************/
//@Author: Adrian "yEnS" Mato Gondelle &amp;amp;amp; Ivan Guardado Castro
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!

//@Author: Brian Dolbec <dolsen@gentoo.org>
/***************************/

$(document).ready(function(){

    for(i=0; i<tabs.length; i++){
        $("#"+tabs[i]).removeClass("active");
        $("div."+tabs[i]).css("display", "none");
    };
    $("#"+tabs[0]).addClass("active");
    $("div."+tabs[0]).fadeIn();

    $(".menu > li").click(function(e){

        var targ = e.target.id;

        for(i=0; i<tabs.length; i++){
            if (tabs[i] == targ){
                $("#"+tabs[i]).addClass("active");
                $("div."+tabs[i]).fadeIn();
            }
            else {
                $("#"+tabs[i]).removeClass("active");
                $("div."+tabs[i]).css("display", "none");
            };
        };

        return false;
    });
});


