const swiperStoris = new Swiper(".stories__swiper", {
  loop: true,
  lazy: true,
  slidesPerView: 2.5,
  spaceBetween: 10,
  autoplay: {
    delay: 2000,
    pauseOnMouseEnter: true,
  },
  freeMode: {
    enabled: true,
    sticky: true,
  },
  breakpoints: {
    576: {
      slidesPerView: 3.5,
      spaceBetween: 15,
    },
    768: {
      slidesPerView: 4,
      spaceBetween: 70,
    },
    992: {
      slidesPerView: 5,
      spaceBetween: 75,
    },
    1200: {
      slidesPerView: 6,
      spaceBetween: 50,
    },
    1400: {
      slidesPerView: 8,
      spaceBetween: 20,
    },
  },
});
const swiperBrands = new Swiper(".brand-swiper", {
  loop: true,
  lazy: true,
  slidesPerView: 2.5,
  spaceBetween: 10,
  autoplay: {
    delay: 2000,
  },
  freeMode: {
    enabled: true,
    sticky: true,
  },
  breakpoints: {
    576: {
      slidesPerView: 3.5,
      spaceBetween: 15,
    },
    768: {
      slidesPerView: 4,
      spaceBetween: 70,
    },
    992: {
      slidesPerView: 5,
      spaceBetween: 75,
    },
    1200: {
      slidesPerView: 6,
      spaceBetween: 50,
    },
    1400: {
      slidesPerView: 7,
      spaceBetween: 48,
    },
  },
});
const swiperHomeProduct = new Swiper(".home-product-swiper", {
  loop: true,
  lazy: true,
  slidesPerView: 1.8,
  spaceBetween: 10,
  // autoplay: {
  //   delay: 2000,
  // },
  freeMode: {
    enabled: true,
    sticky: true,
  },
  breakpoints: {
    576: {
      slidesPerView: 2.5,
    },
    768: {
      slidesPerView: 3,
    },
    992: {
      slidesPerView: 3,
    },
    // 1200: {
    //   slidesPerView: 6,
    // },
    1400: {
      slidesPerView: 4.60,
    },
  },
});
const swiperServices = new Swiper(".services", {
  loop: true,
  lazy: true,
  slidesPerView: 2.5,
  spaceBetween: 10,
  autoplay: {
    delay: 2000,
  },
  freeMode: {
    enabled: true,
    sticky: true,
  },
  breakpoints: {
    576: {
      slidesPerView: 3,
    },
    768: {
      slidesPerView: 4,
    },
    992: {
      slidesPerView: 5,
    },
  },
})
