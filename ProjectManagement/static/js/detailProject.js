$(document).ready(function (){
    var elems = $(".userProject");
    var $newvisibility = $('<i class = "mdi-navigation-more-horiz" id = "viewTask"></i></a>');
    alert("mayor");
    $(".recent-activity-list-text").append($newvisibility);
    for(var i = 0; ele = elems[i]; i++) {
        alert(i);
        if (i > 2) {
            alert(i);
            if (ele.className === 'userProject')
                ele.innerHTML = '';
        }
    }
    //$(".recent-activity-list-text").toggle();
});
