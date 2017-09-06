$(document).ready(function (){
    var elems = $(".userProject");
    var doc= $(".doc");
    var $newvisibility = $('<a class="waves-effect waves-light modal-trigger"  onclick="viewUsers()">Ver Más</a>');
    var $newdoc = $('<a class="waves-effect waves-light modal-trigger" onclick="viewDocuments()" >Ver Más</a>');
    if (elems.length > 2) {
        $(".persons").append($newvisibility);
        for (var i = 0; ele = elems[i]; i++) {
            if (i > 1) {
                if (ele.className === 'userProject')
                    ele.style.display="none";
            }
        }
    }
    if (doc.length > 2 ){
        $(".documents").append($newdoc);
        for (var i = 0; ele = doc[i]; i++) {
            if (i > 1) {
                if (ele.className === 'doc')
                    ele.style.display="none";
            }
        }
    }
});

function viewUsers() {
    $("#ViewUsers").openModal();
}

function viewDocuments() {
    $("#ViewDocuments").openModal();
}
