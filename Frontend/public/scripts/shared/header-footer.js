import {
  overlayVisible,
  overlayHidden,
  mobileMenuVisible,
  mobileMenuHidden,
} from "../funcs/shared.js";
// Menu Mobile Elements (Header)
const openMobileBtn = document.querySelector(".mobile-menu__open-btn");
const menuMobile = document.querySelector(".menu-mobile");
const closeMobileBtn = document.querySelector(".menu-mobile__close-btn");
const overlay = document.querySelector(".overlay");
// Back to top button Element (Footer)
const backToTopBtn = document.getElementById("back-to-top-button");

// Function Open Menu For Mobile
const openMobileBtnHandler = () => {
  mobileMenuVisible(menuMobile, "-right-64", "right-0");
  overlayVisible(overlay, "overlay--visible");
};

// Function Close Menu For Mobile
const closeMobileMenuHandler = () => {
  mobileMenuHidden(menuMobile, "-right-64", "right-0");
  overlayHidden(overlay, "overlay--visible");
};

openMobileBtn.addEventListener("click", openMobileBtnHandler);
closeMobileBtn.addEventListener("click", closeMobileMenuHandler);
overlay.addEventListener("click", closeMobileMenuHandler);

// Back to Top Btn
const backToTopBtnHandler = () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
};
backToTopBtn.addEventListener("click", backToTopBtnHandler);

export { overlay };
