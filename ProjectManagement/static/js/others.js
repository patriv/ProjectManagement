//     var availableTags = [
//       "Club Mercado",
//       "Agruppa",
//       "Directo",
//       "Canopy Verde"
//     ];


// $(function() {

//     $( "#autocomplete" ).autocomplete({
//       source: "get_project"
//     });
//   } );


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

   ////////////////////////////////////////////////////////////////////////////////////////////////
    $( function() {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $( "#autocomplete" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "get_project", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 2 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
  } );

//    $.ajax({
//                url: form.attr("data-forgot-url"),
//                data: {
//                    project: project
//                },
//                type: 'POST',
//                dataType: 'json',
//                success: function (data) {
//                    var emailExist = data.username_exists;
//                    if ((emailExist) === false) {
//                        alert("aquiii")
//
//                    }
//                }
//            });
//
// // function nombre(fic,i) {
// //   // como se llama en el div ---> onchange="nombre(this.value,i-1)
// //   fic = fic.split('\\');
//   alert(fic[fic.length-1]);
//   var input = "#input-"+i;
//   alert(input);
//   $(input).attr("value",fic[fic.length-1]);

// }

// // Agregar más documentos
// $(".chosen").bind("chosen:maxselected", function () {
//     alert("Máximo número de elementos seleccionado")
// });

// function abc(i) {
//   var input = "#input-"+i;
//   var a = $('div[class="btn"]');
//   a.find('input[type="file"]').change(function(){
//     input.val(a[0].files[0].name);
//     input.trigger("change");
//   });
// }








