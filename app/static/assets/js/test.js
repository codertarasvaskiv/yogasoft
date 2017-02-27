$(document).on('click', '.list_view', function(){
    // what you want to happen when mouseover and mouseout
    // occurs on elements that match '.dosomething'
    // info from stackoverflow  VERY NICE
    // http://stackoverflow.com/questions/203198/event-binding-on-dynamically-created-elements
    var info = $(this).attr("data-prod");
    var search_info = $('#search').val();
    $('#ajax').load("../list_view/"+info+'/'+search_info).hide().fadeIn();
});

$('#loadUpdateViewJquery').click(function(){
    var info = $(this).attr("data-prod");
    $('#ajax').load("../edit_product/"+info).hide().fadeIn();
});

$('#clearSearchInfo').click(function(){
    $('#search').val('');
});

$('#like').click(function(){
    var info = $(this).attr("data-prod");
    $.get('/app/like/', {like_info: info}, function(data){
    $('#like_count').html(data);
    $('#like').hide();
    });
});

$('#delete').click(function(){
    var info = $(this).attr("data-prod");
    if(confirm("Are you sure?")){
    $.get('/app/delete_product/', {delete_info: info}, function(data){
    $('#ajax').empty();
    });
    }
});

$('#edit').click(function(){
    var info = $(this).attr("data-prod");
    $('#ajax').load("../edit_product/"+info);
    });

$('.category').click(function(){
    var info = $(this).attr("data-prod");
    $('#ajax').load("../list_view/"+info+"/1");
    });


$('#grid_view').click(function(){
    $('#ajax').load("../grid_view/").hide().fadeIn();
});

$('#search').keyup(function(){
    var info = $(this).val();
    $('#ajax').load("../list_view///"+info).hide().fadeIn();
});




$(document).ready(function() {
    var time = new Date();
    var tim = time.getHours() +':' + time.getMinutes() +':' + time.getSeconds();
        $('#time').text(tim);
    }
);

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});