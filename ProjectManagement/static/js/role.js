$(document).ready(function (){
    /*para pasar el link de modificar al modal*/

    $(document).on("click", ".open-AddBookDialog", function () {
        var myBookId = $(this).data('link-update');
        var myPk = $(this).data('pk');
        $("#form_edit").attr("action", myBookId );
        $("#name").val(myPk);
        $("#nameRol").addClass("active");
        $("#iconRol").addClass("active");
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
        datos = JSON.parse(datos);
        //Proyectos
        $("#id_create_project1").prop("checked", "");
        $("#id_view_project1").prop("checked", "");
        $("#id_update_project1").prop("checked", "");
        $("#id_delete_project1").prop("checked", "");
        //Roles
        $("#id_create_rol1").prop("checked", "");
        $("#id_view_rol1").prop("checked", "");
        $("#id_update_rol1").prop("checked", "");
        $("#id_delete_rol1").prop("checked", "");
        //Users
        $("#id_create_users1").prop("checked", "");
        $("#id_view_users1").prop("checked", "");
        $("#id_update_users1").prop("checked", "");
        $("#id_delete_users1").prop("checked", "");

        $.each(datos, function (i,val) {
            $.each(val, function (j,item) {

                if (item === "add_group"){
                    $("#id_create_rol1").prop("checked", "checked");
                }
                else if (item === "change_group"){
                    $("#id_update_rol1").prop("checked", "checked");
                }
                else if (item === "view_group"){
                    $("#id_view_rol1").prop("checked", "checked");
                }
                else if (item === "delete_group"){
                    $("#id_delete_rol1").prop("checked", "checked");
                }
                 else if (item === "add_user"){
                    $("#id_create_users1").prop("checked", "checked");
                }
                else if (item === "change_user"){
                    $("#id_update_users1").prop("checked", "checked");
                }
                else if (item === "delete_user"){
                    $("#id_delete_users1").prop("checked", "checked");
                }
                else if (item === "view_users"){
                    $("#id_view_users1").prop("checked", "checked");
                }
                else if (item === "add_project"){
                    $("#id_create_project1").prop("checked", "checked");
                }
                else if (item === "change_project"){
                    $("#id_update_project1").prop("checked", "checked");
                }
                 else if (item === "delete_project"){
                    $("#id_delete_project1").prop("checked", "checked");
                }
                else if (item === "view_project"){
                    $("#id_view_project1").prop("checked", "checked");
                }

            });

        });

    });


   /* para pasar el link de eliminar al modal de confirmación*/
    $(document).on("click", ".open-AddBookDialog1", function () {
        var myBookId = $(this).data('link-delete');
        $("#modal2, #acceptDelete").attr("href", myBookId );
    });

});
