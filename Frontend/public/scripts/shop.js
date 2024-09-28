// Filtration elements of products
const selectBoxes = $.querySelectorAll(".select-box")
const selectOptions = $.querySelectorAll(".select-option")

// Filtration elements, product prices
const rangevalue = document.querySelector(".price-slider");
const rangeInputvalue = document.querySelectorAll(".range-input input");
const priceInputvalue = document.querySelectorAll(".price-input input");
let priceGap = 1000;

// 
selectBoxes.forEach((box) => {
    box.addEventListener("click", () => {
        let contentID = box.getAttribute("data-content-id")
        let svgID = box.lastElementChild.id
        $.querySelector(contentID).classList.toggle("select-option--visible")
        $.getElementById(svgID).classList.toggle("rotate-180")
    })
})
// 

// 
function updateSlider() {
    let minp = parseInt(priceInputvalue[0].value);
    let maxp = parseInt(priceInputvalue[1].value);

    rangevalue.style.right = `${(minp / rangeInputvalue[0].max) * 100}%`;
    rangevalue.style.left = `${100 - (maxp / rangeInputvalue[1].max) * 100}%`;
}

for (let i = 0; i < priceInputvalue.length; i++) {
    priceInputvalue[i].addEventListener("input", e => {
        let minp = parseInt(priceInputvalue[0].value);
        let maxp = parseInt(priceInputvalue[1].value);

        if (minp < 0) {
            priceInputvalue[0].value = 0;
            minp = 0;
        }
        if (maxp > 10000) {
            priceInputvalue[1].value = 10000;
            maxp = 10000;
        }
        if (minp > maxp - priceGap) {
            priceInputvalue[0].value = maxp - priceGap;
            minp = maxp - priceGap;
        }

        rangeInputvalue[0].value = minp;
        rangeInputvalue[1].value = maxp;
        updateSlider();
    });
}

for (let i = 0; i < rangeInputvalue.length; i++) {
    rangeInputvalue[i].addEventListener("input", e => {
        let minVal = parseInt(rangeInputvalue[0].value);
        let maxVal = parseInt(rangeInputvalue[1].value);

        if (maxVal - minVal < priceGap) {
            if (e.target.className === "min-range") {
                rangeInputvalue[0].value = maxVal - priceGap;
            } else {
                rangeInputvalue[1].value = minVal + priceGap;
            }
        }

        priceInputvalue[0].value = rangeInputvalue[0].value;
        priceInputvalue[1].value = rangeInputvalue[1].value;
        updateSlider();
    });
}

updateSlider(); // Initialize slider on page load
// 


// 

// 