$(document).ready(function () {

    $("#email").change(function () {
        var email = $(this).val();
        var email_regex = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/; 
       
        $.ajax({
            url: 'ajax/validateUser/',
            data: {
                email: email
            },
            type: 'POST',
            cache: false,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            dataType: 'json',
            success: function (data) {
                if (data.email_exists) {
                    Materialize.toast('Este email ya está registrado, por favor verifique',4000);
                    $("#email").removeClass('valid').addClass('invalid');
                }
                if (email.match(email_regex)=== null){
                    Materialize.toast('Debe introducir un email válido',4000);
                    $("#email").removeClass('valid').addClass('invalid');
                }

            }
        });
    });

   $("#id_username").change(function () {
        var username = $(this).val();
        $.ajax({
            url: 'ajax/validateUser/',
            data: {
                username: username
            },
            type: 'POST',
            cache: false,
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            dataType: 'json',
            success: function (data) {
                if (data.username_exists) {
                    Materialize.toast('Este username ya está registrado, por favor verifique',4000);
                    $("#id_username").removeClass('valid').addClass('invalid');
                }
            }
        });
    })
});


