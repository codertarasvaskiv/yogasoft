$(document).ready(function() {
	$('.carousel').carousel();
	$('.carousel').on('slide.bs.carousel', function () {
		$('.carousel-caption h4').animate({
			marginLeft: "+=100%",
          fontSize: "1px",
			opacity: 0
		}, 50);
	})
	$('.carousel').on('slid.bs.carousel', function () {
		$('.carousel-caption h4').animate({	marginLeft: 0, fontSize: "25px", opacity: 0.8 }, 600);
	})
});

$(document).ready(function() {
	$('.carousel').carousel();
	$('.carousel').on('slide.bs.carousel', function () {
		$('.carousel-caption p').animate({
			marginRight: "+=100%",
          fontSize: "1px",
			opacity: 0
		}, 50);
	})
	$('.carousel').on('slid.bs.carousel', function () {
		$('.carousel-caption p').animate({	marginRight: 0, fontSize: "15px", opacity: 0.8 }, 600);
	})
});

function overlay() {
          el = document.getElementById("overlay");
          el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
      }

      jQuery(document).on('click', '#ov', function (event) {
          event.preventDefault();
          window.location.replace = "/start_project/";
          overlay();
      });

$('#search').keyup(function(){
    var info = $(this).val();
    $('#ajax').load("../search_list/"+info).hide().fadeIn();
});


//this we need to ajax
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