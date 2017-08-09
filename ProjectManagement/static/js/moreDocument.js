function moreDocument() {
  var $newdiv1 = $('<div class="row" ><div class="input-field col l10"><div class="file-field input-field"> ' +
      '<a> <i class="mdi-navigation-close right"></i></a>'+
      '<input class="file-path validate" type="text" /><div class="btn"><span>File</span><input type="file"/></div> ' +
      '</div></div> </div>');
  $("#showDocument").append($newdiv1);

  $('.file-field').each(function() {
  var path_input = $(this).find('input.file-path');
  $(this).find('input[type="file"]').change(function () {
    path_input.val($(this)[0].files[0].name);
    path_input.trigger('change');
  });
});

}