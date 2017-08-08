$(document).ready(function (){
    /*para pasar el link de modificar al modal*/

    $(document).on("click", ".open-AddBookDialog", function () {
        var myBookId = $(this).data('link-update');
        var myPk = $(this).data('pk');
        $("#form_edit").attr("action", myBookId );
        $("#name").val(myPk );
        alert(myPk);
        alert($("#id_create").checked);
        var path = window.location.href.split('/');
        var url= path[0]+"/"+path[1]+"/"+path[2]+"/"+"ajax/role/";

        var datos = $.ajax({
        url: url,
        type:'GET',
        data:{name:myPk},
        cache: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        dataType:'json',
        async:false
    }).responseText;
        alert(datos);
    });

    /* para pasar el link de eliminar al modal de confirmación*/
    $(document).on("click", ".open-AddBookDialog1", function () {
        var myBookId = $(this).data('link-delete');
        $("#modal2, #acceptDelete").attr("href", myBookId );
    });

});
