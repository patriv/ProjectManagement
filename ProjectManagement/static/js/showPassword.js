$(document).ready(function () {
    $("#show-hide-passwd").click(function(e){
      e.preventDefault();
      var current = $(this).attr('action');

      if (current === 'hide'){
        $(this).prev().attr('type','text');
        $(this).removeClass('mdi-action-visibility').addClass('mdi-action-visibility-off').attr('action','show');
      }
      if (current === 'show'){
        $(this).prev().attr('type','password');
        $(this).removeClass('mdi-action-visibility-off').addClass('mdi-action-visibility').attr('action','hide');
      }
    });

});