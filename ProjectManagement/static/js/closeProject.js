$(document).ready(function (){

    var path = window.location.href.split('/');
    var url = path[0]+"/"+path[1]+"/"+path[2]+"/buttoncloseProject/";

    $.ajax({
        url: url,
        origin: 'http://127.0.0.1:8000',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            code: path[4]
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.all_task === data.done_task && data.all_task !== 0) {
                $("#closeProject").removeClass('disabled');
                document.getElementById("closeProject").onclick = function() {
                    document.getElementById("formProject").submit();
                };
            }
            else {
                $("#closeProject").addClass('disabled');
            }
            if (data.status==='Done'){

                $("#closeProject").addClass('disabled').text('Proyecto cerrado');
            }
        },
        error: function (data) {
            alert("Lo sentimos, hay problemas con el servidor. Intente más tarde.");
        }
    });
});
