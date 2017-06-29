$(document).ready(function () {

    $("#password").click(function () {

        Materialize.toast("La contraseña debe ser mayor o igual a ocho caracteres, y no puede ser sólo numérica",3000);
    });

    $("#password2").change(function () {
      var password2 = $(this).val();
      var password = $("#password").val();
      var message1 = "Las contraseñas no coinciden, por favor verifique.";
      if (password2 && (password2 !== password)){
          Materialize.toast(message1,4000);
      }
  });

    $("#password").change(function () {
        var password = $(this).val();
        var message1 = "La contraseña debe ser mayor o igual a ocho caracteres, y no puede ser sólo numérica" ;
        var message2 = "La contraseña no puede ser solo numérica";
        var message3 = "La contraseña debe tener al menos ocho caracteres";
        var regexPassword = /^([a-z]+[0-9]+)|([0-9]+[a-z]+).{8,15}/i;
        var regexNumber = /^\d*$/;
        if (password.match(regexNumber)){
            Materialize.toast(message2,4000);
        }
        else if ((password.length)< 8){
            Materialize.toast(message3, 4000);
        }
        else if (!(password.match(regexPassword))) {
            Materialize.toast(message1,4000);
        }
    });

});