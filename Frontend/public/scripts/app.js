// Scripts :)
const $ = document

// Menu Mobile Elements 
const openMobileBtn = $.querySelector(".header-logo__hamburger")
const menuMobile = $.querySelector(".menu-mobile")
const closeMobileBtn = $.querySelector(".menu-mobile")
const overlay = $.querySelector(".overlay")

// Function Open Menu For Mobile
const openMobileBtnHandler = () => {
    menuMobile.classList.remove("-right-64")    
    menuMobile.classList.add("right-0")    
    overlay.classList.add("overlay--visible")
}

// Function Close Menu For Mobile
const closeMobileBtnHandler = () => {
    menuMobile.classList.add("-right-64")    
    menuMobile.classList.remove("right-0")    
    overlay.classList.remove("overlay--visible")
}

openMobileBtn.addEventListener("click", openMobileBtnHandler)
closeMobileBtn.addEventListener("click", closeMobileBtnHandler)
overlay.addEventListener("click", closeMobileBtnHandler)