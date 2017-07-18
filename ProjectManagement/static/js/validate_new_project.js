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
        var date_end = $(this).val();
        alert(date_end);
        var date_start = $("#start").val();
        alert(date_end);
        alert(date_end < date_start);
        if (date_end < date_start){
            Materialize.toast('La fecha de culminación del proyecto no puede ser anterior a la de inicio.',4000);

        }
    })
});


