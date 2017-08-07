function status(name) {
    var a = ['In Progress','Technical Review','Functional Review', 'Customer Acceptance','Done'];
    $.each(a, function (i,val) {
        if (val == name){
            $('#status').append('<option value='+ val +'selected>'+val+'</option>');
        }
        else {
            $('#status').append('<option value='+ val +'>'+val+'</option>');
        }

    })

}