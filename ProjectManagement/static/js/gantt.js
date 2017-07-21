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


    function selectHandler() {
        var selection=chart.getSelection()[0];

        if (selection){
            alert('You selected ' + data.getValue(selection.row, 0));
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

google.charts.load('current', {'packages':['gantt']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    data.addColumn('string', 'Resource');
    data.addColumn('date', 'Start Date');
    data.addColumn('date', 'End Date');
    data.addColumn('number', 'Duration');
    data.addColumn('number', 'Percent Complete');
    data.addColumn('string', 'Dependencies');

    data.addRows([
        ['2014Spring', 'Tarea 1', 'spring',
            new Date(2014, 2, 22), new Date(2014, 5, 20), null, 100, null],
        ['2014Summer', 'Tarea 2', 'summer',
            new Date(2014, 5, 21), new Date(2014, 8, 20), null, 100, null],
        ['2014Autumn', 'Tarea 3', 'autumn',
            new Date(2014, 8, 21), new Date(2014, 11, 20), null, 100, null],
        ['2014Winter', 'Tarea 4', 'winter',
            new Date(2014, 11, 21), new Date(2015, 2, 21), null, 100, null],
        ['2015Spring', 'Tarea 5', 'spring',
            new Date(2015, 2, 22), new Date(2015, 5, 20), null, 50, null],
        ['2015Summer', 'Tarea 6', 'summer',
            new Date(2015, 5, 21), new Date(2015, 8, 20), null, 0, null],
        ['2015Autumn', 'Tarea 7', 'autumn',
            new Date(2015, 8, 21), new Date(2015, 11, 20), null, 0, null],
        ['2015Winter', 'Tarea 8', 'winter',
            new Date(2015, 11, 21), new Date(2016, 2, 21), null, 0, null],
        ['Football', 'Tarea 9', 'sports',
            new Date(2014, 8, 4), new Date(2015, 1, 1), null, 100, null],
        ['Baseball', 'Tarea 10', 'sports',
            new Date(2015, 2, 31), new Date(2015, 9, 20), null, 14, null],
        ['Basketball', 'Tarea 11', 'sports',
            new Date(2014, 9, 28), new Date(2015, 5, 20), null, 86, null],
        ['Hockey', 'Tarea 12', 'sports',
            new Date(2014, 9, 8), new Date(2015, 5, 21), null, 89, null]
    ]);

    var options = {
        height: 400,
        gantt: {
            trackHeight: 30
        }
    };

    var chart = new google.visualization.Gantt(document.getElementById('gantt_chart'));

    chart.draw(data, options);
}
