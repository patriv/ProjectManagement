$(document).ready(function (){

   /* para pasar el link de eliminar al modal de confirmación*/
    $(document).on("click", ".open-AddBookDialog1", function () {
        var myBookId = $(this).data('link-delete');
        $("#modal2, #acceptDelete").attr("href", myBookId );
    });

});
