$(document).ready(function (){
    /*para pasar el link de modificar al modal*/

    $(document).on("click", ".open-AddBookDialogTask", function () {

        var myPk = $(this).data('pk');
        var path = window.location.href.split('/');
        var url= path[0]+"/"+path[1]+"/"+path[2]+"/"+"detail-task/"+path[4];
        var datos = $.ajax({
            url: url,
            type:'GET',
            data:{code:myPk},
            cache: false,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            dataType:'json',
            async:false
        }).responseText;
        datos = JSON.parse(datos);
        //Proyectos

        $("#nameTask").text(datos.name);
        $("#responsableTask").text(datos.responsable);
        $("#statusTask").text(datos.status);
        $("#descriptionTask").text(datos.description);

    });



});
