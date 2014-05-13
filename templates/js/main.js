$(document).ready(function(){
    //item/node object
    $('#signin-form').hide();
    $('#saved').hide();

    $('#signin-button').click(function(event){
        event.preventDefault();
        $('#signin-form').slideDown();
        $('#signin-button').toggle();
    })

    function Node (nest_level, order) {
        this.nest_level = nest_level
        this.order = order
        this.content = ''
        this.html = ''
        this.pack() = function() {
            return this
        }
    }


    var nest_level = 0;
    var item_html = 
           ["<div class = 'item-container'>", 
            "<div class = 'item offset-0'>",
            "  <form class = 'item-form'>",
            "  <span class = 'item-button-group'>",
            "    <button class = 'item-button-1'>Del</button>",
            "    <button class = 'item-button-2'>Jmp</button>",
            "    <button class = 'item-button-3 new-sibling-button'>Sib</button>",
            "    <button class = 'item-button-4 new-child-button'>Ch</button>",
            "  </span>",
            "  <span class = 'item-textarea-container'>",
            "   <textarea rows='1' class = 'item-textarea'></textarea>",
            "   <input type = 'hidden' class = 'item-nest-level' value = '0'>",
            "   <input type = 'hidden' class = 'item-id' value = '1'>",
            "   <input type = 'hidden' class = 'item-order' value = '0'>",
            "  </span>",
            "  </form>",
            "</div>",
            "</div>"].join('\n')
    

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


    $('.new-node').click(function (event){
        event.preventDefault();
        var item = $(this).closest('.item').clone(true);
        var item_container = $('<div></div>').append(item);
        item_container.addClass('item-container');
        var new_sibling = $(this).closest('.item-container').after(item_container);
        var offset_string = $(this).closest('.item').attr('class').slice(-1);
        var offset = parseInt(offset_string, 10);
        var order = $(this).closest('.item').find('.item-order').val();
        var id = $('.item').length + 1;
        new_sibling.find('.item_textarea').val('');
        new_sibling.find('.item-nest-level').val(offset);
        new_sibling.find('.item-order').val(order);
        new_sibling.find('.item-id').val(id);
        $('.item-textarea').autosize(); 
        $('.item-textarea').trigger('autosize.resize'); 
    });


    $('.page').on('click', '.new-sibling-button', function (event){
        event.preventDefault();
        var item = $(item_html);
        var new_sibling = $(this).closest('.item-container').after(item);
        var offset_string = $(this).closest('.item').find('.item-nest-level').val();
        var offset = parseInt(offset_string, 10);
        var id = $('.item').length + 1;
        item.find('.item-textarea').val('');
        item.find('.item-nest-level').val(offset);
        item.find('.item-id').val(id);
        updateOrder();
        $('.item-textarea').autosize(); 
        $('.item-textarea').trigger('autosize.resize'); 
    });

    $('.page').on('click', '.new-child-button', function (event){
        event.preventDefault();
        var item = $(item_html);
        var id = $('.item').length + 1;
        var offset_string = $(this).closest('.item').find('.item-nest-level').val();
        var offset = parseInt(offset_string, 10) + 1;
        var new_child = $(this).closest('.item').after(item);
        $('.item-textarea').trigger('autosize.resize'); 
        item.find('.item-textarea').val('');
        item.find('.item-nest-level').val(offset);
        item.find('.item-id').val(id);
        updateOrder();
        $('.item-textarea').autosize(); 
        $('.item-textarea').trigger('autosize.resize'); 
    });

    $('.delete-button').click(function (event)  {
        event.preventDefault();
        $(this).hide();
        $(this).siblings('.jump-button').hide();
        $(this).siblings('.confirm-delete-button').show();
    });


    $('.confirm-delete-button').click(function (event)  {
        event.preventDefault();
        $(this).closest('.item').hide();
    });


    $('.jump-button').click(function (event)  {
        event.preventDefault();
        var item = $(this).closest('.item').hide();
    });

    $('.save').click(function (event) {
        event.preventDefault();
        var url = $(this).attr('href');
        var item_list = [];
        var number_items = 0;
        $('.item').each( function () {
            console.log($(this))
            number_items = number_items + 1;
            var item = {
                'content' : $(this).find('.item-textarea').val(),
                'id' : $(this).find('.item-id').val(),
                'nest_level' : $(this).find('.item-nest-level').val(),
                'order' : number_items,
            }
            item_list.push(item);

        });
        console.log(item_list)
        $.ajax({
            type: 'POST',
            url: url,
            data: {number_items: number_items,
                data : JSON.stringify({items : item_list})}
        }).done(function() {
                $('#saved').show(800).delay(3000).fadeOut();
        });
    });

    function updateOrder() {
        var i = 0;
        $('.item').each( function () {
            i = i + 1;
            $(this).find('order').val(i);
            var nest_level = $(this).find('.item-nest-level').val().toString();
            $(this).removeClass().addClass('item offset-'+nest_level)
        });
    };

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

