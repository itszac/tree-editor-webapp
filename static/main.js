$(document).ready(function(){
    var nest_level = 0;

    $('.item-textarea').autosize(); 

    $.ajaxSetup({
        crossDomain:false,
        beforeSend: function(xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    })


    $('.new-sibling-button').click(function (event){
        event.preventDefault();
        var item = $(this).closest('.item').clone(true, true);
        item.find('.item-textarea:first').autosize();
        var item_container = $('<div></div>').append(item);
        item_container.addClass('item-container');
        var new_sibling = $(this).closest('.item-container').after(item_container);
        $('.item-textarea').autosize(); 
        $('.item-textarea').trigger('autosize.resize'); 
    });

    $('.new-child-button').click(function  (event) {
        event.preventDefault();
        var item = $(this).closest('.item').clone(true, true);
        item.find('.item-textarea:first').autosize();
        var offset_string = $(this).closest('.item').attr('class').slice(-1);
        var offset = parseInt(offset_string, 10) + 1;
        item.removeClass().addClass('item offset-' + offset.toString());
        var item_container = $('<div></div>').append(item);
        item_container.addClass('item-container');
        var new_child = $(this).closest('.item').after(item_container);
        $('.item-textarea').trigger('autosize.resize'); 
    });

    $('.delete-button').click(function (event)  {
        event.preventDefault();
        $('.delete-button').hide();
        $('.confirm-delete-button').show();
    });


    $('.confirm-delete-button').click(function (event)  {
        event.preventDefault();
        var item = $(this).closest('.item').hide();
    });


    $('.jump-button').click(function (event)  {
        event.preventDefault();
        var item = $(this).closest('.item').hide();
    });

    $('.save').click(function (event) {
        event.preventDefault();
        var url = $(this).attr('href');
        console.log(url);
        console.log($(this));
        console.log($(this).attr('class'));
        var item_list = [];
        $('.item').each( function () {
            var item = {
                'value' : $(this).closest('.item-textarea').value,
                'id' : $(this).closest('.item-id').value,
                'nest_level' : $(this).closest('.item-nest-level').value
            }
            item_list.push(item);

        });
        console.log(item_list)
        $.ajax({
            type: 'POST',
            url: url,
            data: {data : JSON.stringify(item_list)}
        }).done(function() {
                alert( "Data Saved" );
        });
    });

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

