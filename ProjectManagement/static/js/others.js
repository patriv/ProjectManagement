    var availableTags = [
      "Club Mercado",
      "Agruppa",
      "Directo",
      "Canopy Verde"
    ];


$( function() {

    $( "#autocomplete" ).autocomplete({
      source: availableTags
    });
  } );


// $(document).ready(function() {
//         $(function() {
//                 $("#autocomplete").autocomplete({    
//                 source : function(request, response) {
//                 $.ajax({
//                         url : "resources/projects.json",
//                         type : "GET",
//                         data : {
//                                 term : request.term
//                         },
//                         dataType : "json",
//                         success : function(data) {
//                                 response(data);
//                         }
//                 });
//         }
// });
// });
// });