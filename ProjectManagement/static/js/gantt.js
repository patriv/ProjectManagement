google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBarColors);

var datos = $.ajax({
    url:'bar',
    type:'POST',
    cache: false,
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    dataType:'json',
    async:false
}).responseText;

datos = JSON.parse(datos);

function datailProject(name) {

    var nameProject = name;

    var path = window.location.href.split('/');

    var url = path[0]+"/"+path[1]+"/"+path[2]+"/ajax/detailProject/";

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
            if (data.project) {
                $("#project").text(data.name);
                $("#start").text(data.start);
                $("#end").text(data.end);
                $("#employ").text(data.responsable);
                $("#client").text(data.client);
                $("#status").text(data.status);

            }
            else {
                alert("error");
            }
        },
        error: function (data) {
            alert("Lo sentimos, hay problemas con el servidor. Intente más tarde.");
        }
    });
}

function drawBarColors() {
    var data = google.visualization.arrayToDataTable(datos);

    var options = {
        title: 'Proyectos IDBC Group',
        titlePosition: 'out',

        chartArea: {width: '70%'},
        colors: ['#965a89', '#E6B0B8'],
        hAxis: {
            title: 'Duración (días)',
            minValue: 0
        },
        vAxis: {
            title: 'Proyectos'
        },
        height: 280,
        legend: {alignment:'center', position: "top", maxLines: 3},
        bar: { groupWidth: '75%' }

    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    google.visualization.events.addListener(chart, 'error', function (googleError) {
      google.visualization.errors.removeError(googleError.id);
      $("#chart_div").empty().append('<img src="../../static/images/Status-image-missing-icon.png"><div>NO HAY GRÁFICO DISPONIBLE</div>');
  });



    function selectHandler() {

        var selection=chart.getSelection()[0];
        alert (selection);


        // $.each(datos, function (i, val) {
        //    alert(val[0]);
        //
        // });
        if (selection){
            datailProject(data.getValue(selection.row, 0));
            info = data.getValue(selection.row,0);
            var chart_div = document.getElementById('detail');
            //document.getElementById('detail').innerHTML = data.getValue(selection.row,0);

            document.getElementById('detail').style.display = 'block';
            document.getElementById('table_task').style.display = 'block';

        }

    }

    // Listen for the 'select' event, and call my function selectHandler() when
    // the user selects something on the chart.
    google.visualization.events.addListener(chart, 'select', selectHandler);
    chart.draw(data, options);
}

// Diagrama de Gantt

