google.charts.load('current', {'packages':['gantt']});
google.charts.setOnLoadCallback(drawChart);
var path = window.location.href.split('/');
var url= path[0]+"/"+path[1]+"/"+path[2]+"/"+"ajax/gantt";
var datos = $.ajax({
    url: url,
    type:'POST',
    cache: false,
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    dataType:'json',
    async:false
}).responseText;
alert(datos);

//datos = JSON.parse(datos);

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
            new Date(2014, 9, 8), new Date(2015, 5, 21), null, 89, 'Basketball']
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
