google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBarColors);

function drawBarColors() {
      var data = google.visualization.arrayToDataTable([
        ['Proyecto', 'Estimada', 'Real'],
        ['Agruppa', new Date(2017, 3, 12), new Date(2017, 2, 9)],
        ['Club Mercado', new Date(2017, 4, 20), new Date(2017, 5, 25)],
        ['Directo', new Date(2017, 6, 15), new Date(2017, 5, 10)]
      ]);

      var options = {
        title: 'Proyectos IDBC Group',
        chartArea: {width: '50%'},
        colors: ['#b0120a', '#01579b'],
        hAxis: {
          title: 'Duración',
          minValue: new Date(2015, 0, 1)
        },
        vAxis: {
          title: 'Proyectos'
        }
      };
      var chart = new google.visualization.BarChart(document.getElementById('chart_div'));


      function selectHandler() {
          var selectedItem = chart.getSelection()[0];

          if (selectedItem) {
              var value = data.getValue(selectedItem.row, selectedItem.column);

              document.getElementById('detail').style.display = 'block';
              document.getElementById('table_task').style.display = 'block';
              $('#table_task').addClass("min-tabla");
               $('#filas').style.width = '136px';

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
        ['2014Spring', 'Spring 2014', 'spring',
         new Date(2014, 2, 22), new Date(2014, 5, 20), null, 100, null],
        ['2014Summer', 'Summer 2014', 'summer',
         new Date(2014, 5, 21), new Date(2014, 8, 20), null, 100, null],
        ['2014Autumn', 'Autumn 2014', 'autumn',
         new Date(2014, 8, 21), new Date(2014, 11, 20), null, 100, null],
        ['2014Winter', 'Winter 2014', 'winter',
         new Date(2014, 11, 21), new Date(2015, 2, 21), null, 100, null],
        ['2015Spring', 'Spring 2015', 'spring',
         new Date(2015, 2, 22), new Date(2015, 5, 20), null, 50, null],
        ['2015Summer', 'Summer 2015', 'summer',
         new Date(2015, 5, 21), new Date(2015, 8, 20), null, 0, null],
        ['2015Autumn', 'Autumn 2015', 'autumn',
         new Date(2015, 8, 21), new Date(2015, 11, 20), null, 0, null],
        ['2015Winter', 'Winter 2015', 'winter',
         new Date(2015, 11, 21), new Date(2016, 2, 21), null, 0, null],
        ['Football', 'Football Season', 'sports',
         new Date(2014, 8, 4), new Date(2015, 1, 1), null, 100, null],
        ['Baseball', 'Baseball Season', 'sports',
         new Date(2015, 2, 31), new Date(2015, 9, 20), null, 14, null],
        ['Basketball', 'Basketball Season', 'sports',
         new Date(2014, 9, 28), new Date(2015, 5, 20), null, 86, null],
        ['Hockey', 'Hockey Season', 'sports',
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
