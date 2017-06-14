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

   ////////////////////////////////////////////////////////////////////////////////////////////////
  $( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    function split( val ) {
      return val.split( /x\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }

    $( "#requerida_por" )
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          // delegate back to autocomplete, but extract the last term
          response( $.ui.autocomplete.filter(
            availableTags, extractLast( request.term ) ) );
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          var x = " x ";
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join(  x );
          terms.chosen();
      
          return false;
        }
      });
  } );


function nombre(fic,i) {
  // como se llama en el div ---> onchange="nombre(this.value,i-1)
  fic = fic.split('\\');
  alert(fic[fic.length-1]);
  var input = "#input-"+i;
  alert(input);
  $(input).attr("value",fic[fic.length-1]);

}

// Agregar más documentos
$(".chosen").bind("chosen:maxselected", function () {
    alert("Máximo número de elementos seleccionado")
});

function abc(i) {
  var input = "#input-"+i;
  var a = $('div[class="btn"]');
  a.find('input[type="file"]').change(function(){
    input.val(a[0].files[0].name);
    input.trigger("change");
  });
}








