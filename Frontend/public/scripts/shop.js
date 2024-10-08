import {toggleSelect , selectOption} from "./ui/ui-handlers.js";

// Filtration elements, product prices
const rangevalue = document.querySelector(".price-slider");
const rangeInputvalue = document.querySelectorAll(".range-input input");
const priceInputvalue = document.querySelectorAll(".price-input input");
let priceGap = 1000;


// Filtration elements of products
const selectElementsHeaders = document.querySelectorAll(".panel-select__header");
// Filtration Funcs
const handleSelect = el => {
    const type = el.dataset.type
    const selectElement = document.querySelector(`.panel-select--${type}`)
    const selectedElement = document.querySelector(`.panel-select__selected-option--${type}`)
    const icon = document.querySelector(`.panel-select__icon--${type}`)
    const optionWrapperElement = document.querySelector(`.panel__options-wrapper--${type}`)
    const optionElements = document.querySelectorAll(`panel__option--${type}`)

    optionElements.forEach(option => {
        option.addEventListener("click", () => {
            selectOption(type , selectElement , selectedElement , optionElements , option , "panel-select--active", "select-option__item--active" )
            toggleSelect(icon , optionWrapperElement , "panel-select--active")
        })
    })
    optionElements.forEach(option => {
        option.addEventListener("click" , () => {
            option.classList.add("select-option__item--active")
        })
    })
    el.addEventListener("click" , () => {
        toggleSelect(icon , optionWrapperElement , "panel-select--active")
    })
}

selectElementsHeaders.forEach(el => handleSelect(el))


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