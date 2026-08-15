document.addEventListener("DOMContentLoaded", function(){
	var SwiperTestimonial = new Swiper(".swiper-testimonial", {
		slidesPerView: 1,
		spaceBetween: 20,
		loop: true,
		grabCursor: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
			pauseOnMouseEnter: false,
		},
		breakpoints: {
			0: {
				slidesPerView: 1
			},
			767: {
				slidesPerView: 2
			},
			991: {
				slidesPerView: 1
			}
		}
	});
});

document.querySelectorAll(".swiper-services-wrapper").forEach(wrapper => {
	new Swiper(wrapper.querySelector(".swiper-services"), {
		slidesPerView: 3,
		spaceBetween: 20,
		loop: true,
		loopedSlides: 3,
		grabCursor: false,
		observer: true,
		observeParents: true,
		speed: 1000,

		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
			pauseOnMouseEnter: false,
		},

		pagination: {
			el: ".swiper-services .swiper-pagination",
			clickable: true,
			renderBullet: function (index, className) {
				return `<span class="${className}"></span>`;
			},
		},

		navigation: {
			nextEl: ".swiper-services-wrapper .swiper-button-next",
			prevEl: ".swiper-services-wrapper .swiper-button-prev",
		},

		breakpoints: {
			0: {
				slidesPerView: 1,
			},
			991: {
				slidesPerView: 3,
			},
		},
	});
});

document.addEventListener("DOMContentLoaded", function(){
	var SwiperPartner = new Swiper(".swiper-partner", {
		slidesPerView: 2,
		spaceBetween: 20,
		loop: true,
		grabCursor: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
			pauseOnMouseEnter: false,
		},
		breakpoints: {
			0: {
				slidesPerView: 2
			},
			767: {
				slidesPerView: 3
			},
			991: {
				slidesPerView: 5
			}
		}
	});
});