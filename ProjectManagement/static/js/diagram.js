google.charts.load('current', {'packages':['gantt']});
google.charts.setOnLoadCallback(drawChart);
var path = window.location.href.split('/');
var url= path[0]+"/"+path[1]+"/"+path[2]+"/"+"ajax/gantt/";

var datos = $.ajax({
    url: url,
    type:'GET',
    data:{project:path[4]},
    cache: false,
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    dataType:'json',
    async:false
}).responseText;


datos = JSON.parse(datos);

var x = [];


$.each(datos, function (i, val) {
    var y = [];
    var date_start = val[2].split('-');
    var end_date = val[3].split('-');
    var start = new Date(date_start[0],date_start[1]-1,date_start[2]);
    var end = new Date(end_date[0],end_date[1]-1,end_date[2]);

    y.push(val[0],val[1],start,end,val[4],val[5],val[6]);
    x.push(y);
});


function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    //data.addColumn('string', 'Resource');
    data.addColumn('date', 'Start Date');
    data.addColumn('date', 'End Date');
    data.addColumn('number', 'Duration');
    data.addColumn('number', 'Percent Complete');
    data.addColumn('string', 'Dependencies');

    data.addRows(x);

    if (data.getNumberOfRows()<3){
        var options = {
        height: data.getNumberOfRows() * 200,
        gantt: {
            trackHeight: 30
        }
    };
}
    else{
         var options = {
        height: data.getNumberOfRows() * 35,
        gantt: {
            trackHeight: 30
        }
    }


    }
   

    var chart = new google.visualization.Gantt(document.getElementById('gantt_chart'));
    google.visualization.events.addListener(chart, 'error', function (googleError) {
      google.visualization.errors.removeError(googleError.id);
      $("#gantt_chart").empty().append('<img src="../../static/images/Status-image-missing-icon.png" ><div>NO HAY GRÁFICO DISPONIBLE</div>');
  });


    chart.draw(data, options);

}
