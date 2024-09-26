// Scripts :)
const $ = document

// Menu Mobile Elements 
const openMobileBtn = $.querySelector(".mobile-menu__open-btn")
const menuMobile = $.querySelector(".menu-mobile")
const closeMobileBtn = $.querySelector(".menu-mobile__close-btn")
const overlay = $.querySelector(".overlay")

// Function Open Menu For Mobile
const openMobileBtnHandler = () => {
    menuMobile.classList.remove("-right-64")    
    menuMobile.classList.add("right-0")    
    overlay.classList.add("overlay--visible")
}

// Function Close Menu For Mobile
const closeMobileMenuHandler = () => {
    menuMobile.classList.add("-right-64")    
    menuMobile.classList.remove("right-0")    
    overlay.classList.remove("overlay--visible")
}

/////////////////////////////////////////////////////////////////
// Back to Top Btn
const backToTopBtn = $.getElementById("back-to-top-button")

backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
})

///////////////////////////////////////////////////////////////////


openMobileBtn.addEventListener("click", openMobileBtnHandler)
closeMobileBtn.addEventListener("click", closeMobileMenuHandler)
overlay.addEventListener("click", closeMobileMenuHandler)