$(document).ready(function () {

    $("#name").change(function () {
        var name = $(this).val();
        $.ajax({
            url: 'ajax/name',
            data: {
                name: name
            },
            type: 'POST',
            cache: false,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            dataType: 'json',
            success: function (data) {
                if (data.name_exists) {
                    Materialize.toast('El nombre del proyecto ya existe, por favor verifique',4000);
                    $("#name").removeClass('valid').addClass('invalid');
                }
            }
        });
    });

    $("#end").change(function () {
        var date_end = $(this).val().split('-');
        var date_start = $("#start").val().split('-');
        var start = new Date(date_start[0],date_start[1],date_start[2]);
        var end = new Date(date_end[0],date_end[1],date_end[2]);
        if (end < start) {
            Materialize.toast('La fecha de culminación del proyecto no puede ser anterior a la de inicio.',4000);
        }
    })
});


