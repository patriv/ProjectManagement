$(document).ready(function (){
    var elems = $(".userProject").length;
    alert(elems);
    if (elems > 3){
        var $newvisibility = $('<i class = "mdi-navigation-more-horiz" id = "viewTask"></i></a>');
        alert("mayor");
        $(".recent-activity-list-text").append($newvisibility);
        for(var i = 0; ele = $('.userProject')[i]; i++) {
            alert(i);
            if (i > 2) {
                alert(i);
                if (ele.className === 'userProject')
                    ele.innerHTML = '';
            }
        }
        //$(".recent-activity-list-text").toggle();
    }
});
