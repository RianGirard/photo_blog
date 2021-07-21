$(function () {
    $("#fileupload").fileupload({
        datatype: 'json',
        done: function (e, data) {  
            $.each(data.result.files, function (index, file){
                $('<p></p>').text(file.name).appendTo(document.body);
            });
        }
    });
});