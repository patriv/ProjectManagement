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

function detailTable(name) {
    var nameProject=name;
    var path = window.location.href.split('/');
    var url = path[0]+"/"+path[1]+"/"+path[2]+"/ajax/table/";

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
                var t = $("#data-table-simple").DataTable();
                t.clear().draw();
                $.each(data.task,function (i,val) {

                    t.row.add([val[0],val[1],val[2]+" "+val[3],val[4],
                        val[5],val[6],val[7],val[8]]).draw();
                });

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
            title: 'Proyectos',
            minValue: 0

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



    function selectHandler(e) {
        var parts = e.targetID.split('#');

        if (parts.indexOf('label') >= 0) {
            var idx = parts[parts.indexOf('label') + 1];
            info = data.getValue(parseInt(idx), 0);
            datailProject(info);
            detailTable(info);
            document.getElementById('detail').style.display = 'block';
            document.getElementById('table_task').style.display = 'block';
        }

        // var selection=chart.getSelection()[0];
        //
        // if (selection){
        //     info = data.getValue(selection.row,0);
        //     datailProject(info);
        //     detailTable(info);
        //
        //     var chart_div = document.getElementById('detail');
        //     //document.getElementById('detail').innerHTML = data.getValue(selection.row,0);
        //
        //     document.getElementById('detail').style.display = 'block';
        //     document.getElementById('table_task').style.display = 'block';
        //
        // }

    }

    // Listen for the 'select' event, and call my function selectHandler() when
    // the user selects something on the chart.
    google.visualization.events.addListener(chart, 'click', selectHandler);
     var chartContainer = document.getElementById('chart_div');
    google.visualization.events.addListener(chart, 'ready', function (e) {
      // modify x-axis labels
     

        var labels = chartContainer.getElementsByTagName('text');
        alert(labels);
       
            Array.prototype.forEach.call(labels, function(label) {

             if (label.getAttribute('text-anchor') === 'end') {
                label.style.fontWeight = 'bold';
                label.style.cursor = 'pointer';
                }
          


      });

    });

    chart.draw(data, options);

}


