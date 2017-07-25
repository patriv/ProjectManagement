function kwargs(name) {
    var nameProject = name;

    var path = window.location.href.split('/');

    var url = path[0]+"/"+path[1]+"/"+path[2]+"/ajax/kwargs/";

    $.ajax({
        url: url,
        origin: 'http://127.0.0.1:8000',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            nameProject: nameProject
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            location.href=path[0]+"/"+path[1]+"/"+path[2]+"/detail-project/"+ data.code;
        },
        error: function (data) {
            alert("Lo sentimos, hay problemas con el servidor. Intente más tarde.");
        }
    });

}
