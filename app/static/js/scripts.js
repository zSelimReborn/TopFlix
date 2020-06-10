(function($) {
	$(document).ready(function() {
		"use strict";

	// PRELOADER
		loader()
		function loader(_success) {
			var obj = document.querySelector('.preloader'),
			inner = document.querySelector('.inner .percentage'),
			page = document.querySelector('body');
			obj.classList.remove('page-loaded');
			page.classList.add('page-loaded');
			var w = 0,
				t = setInterval(function() {
					w = w + 1;
					inner.textContent = w;
					if (w === 100){
						obj.classList.add('page-loaded');
						page.classList.remove('page-loaded');
						clearInterval(t);
						w = 0;
						if (_success){
							return _success();
						}
					}
				}, 20);
		}

		// HIDE NAVBAR
		$(window).on("scroll touchmove", function () {
		$('.navbar').toggleClass('hide', $(document).scrollTop() > 30);
		});


});

})(jQuery);
