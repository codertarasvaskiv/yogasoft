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