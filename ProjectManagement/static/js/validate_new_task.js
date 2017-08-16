$(document).ready(function () {
    $("#id_name").change(function () {
        var name = $(this).val();
        var path = window.location.href.split('/');
        var url = path[0]+"/"+path[1]+"/"+path[2]+"/ajax/nameTask/";
        $.ajax({
            url: url,
            data: {
                name: name,
                code:path[4]
            },
            type: 'GET',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            dataType: 'json',
            success: function (data) {
                if (data.name_exists) {
                    $("#id_name").removeClass('valid').addClass('invalid');
                    Materialize.toast('Esta tarea ya existe para este proyecto, por favor, verifique',4000);

                }
            }
        });

    });

    $("#end").change(function () {
        var date_end = $(this).val().split('-');
        var date_start = $("#start").val().split('-');
        var start = new Date(date_start[2],date_start[1],date_start[0]);
        var end = new Date(date_end[2],date_end[1],date_end[0]);
        if (end < start) {
            Materialize.toast('La fecha de culminación del proyecto no puede ser anterior a la de inicio.',4000);
        }
    })
});


