function moreDocument() {
  var $newdiv1 = $('<li class="file-field input-field">' +
      ' <i class="mdi-navigation-close right close-document"></i>'+
      '<input class="file-path validate document" type="text" />'+'<span class="col l6"> </span>'+
      '<input class="description" type="text" name="description" placeholder="Descripción">'+
      '<div class="btn"><span>File</span><input type="file" name="file" /></div>'+
      '</li>');
  $("#showDocument").append($newdiv1);

  $('.file-field').each(function() {
  var path_input = $(this).find('input.file-path');
  $(this).find('input[type="file"]').change(function () {
    path_input.val($(this)[0].files[0].name);
    path_input.trigger('change');
  });
});

    $(".close-document").click(function() {
        $(this).parents('li').first().remove();
    });

}
                          