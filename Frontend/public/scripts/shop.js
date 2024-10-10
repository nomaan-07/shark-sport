import { toggleSelect, selectOption } from "./ui/ui-handlers.js";
import { overlay } from "./shared/header-footer.js";
import {
  overlayVisible,
  overlayHidden,
  mobileMenuVisible,
  mobileMenuHidden,
} from "./funcs/shared.js";
// Filtration elements, product prices
const rangevalue = document.querySelector(".price-slider");
const rangeInputvalue = document.querySelectorAll(".range-input input");
const priceInputvalue = document.querySelectorAll(".price-input input");
let priceGap = 1000;
// Filtration elements of products
const selectElementsHeaders = document.querySelectorAll(
  ".panel-select__header"
);
// Filter Menu Mobile Elements
const openfilterBtn = document.getElementById("filter-btn");
const closeFilterBtn = document.getElementById("close-filter-btn");
const mobileMenuFilter = document.querySelector(".mobile-menu-filter");

// Filtration Funcs
const handleSelect = (el) => {
  const type = el.dataset.type;
  const selectElement = document.querySelector(`.panel-select--${type}`);
  const selectedElement = document.querySelector(
    `.panel-select__selected-option--${type}`
  );
  const icon = document.querySelector(`.panel-select__icon--${type}`);
  const optionWrapperElement = document.querySelector(
    `.panel__options-wrapper--${type}`
  );
  const optionElements = document.querySelectorAll(`.panel__option--${type}`);

  optionElements.forEach((option) => {
    option.addEventListener("click", () => {
      selectOption(
        selectElement,
        selectedElement,
        optionElements,
        option,
        type,
        "text-orangeBrand",
        "select-option--visible"
      );
      toggleSelect(icon, optionWrapperElement, "text-orangeBrand");
    });
  });
  el.addEventListener("click", () => {
    toggleSelect(icon, optionWrapperElement, "text-orangeBrand");
  });
};

selectElementsHeaders.forEach((el) => handleSelect(el));

const openFilterMenuHandler = () => {
  mobileMenuVisible(mobileMenuFilter, "-right-[300px]", "right-0");
  overlayVisible(overlay, "overlay--visible");
};

const closeFilterMenuHandler = () => {
  mobileMenuHidden(mobileMenuFilter, "-right-[300px]", "right-0");
  overlayHidden(overlay, "overlay--visible");
};

function updateSlider() {
  let minp = parseInt(priceInputvalue[0].value);
  let maxp = parseInt(priceInputvalue[1].value);

  rangevalue.style.right = `${(minp / rangeInputvalue[0].max) * 100}%`;
  rangevalue.style.left = `${100 - (maxp / rangeInputvalue[1].max) * 100}%`;
}

for (let i = 0; i < priceInputvalue.length; i++) {
  priceInputvalue[i].addEventListener("input", (e) => {
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
  rangeInputvalue[i].addEventListener("input", (e) => {
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

openfilterBtn.addEventListener("click", openFilterMenuHandler);
closeFilterBtn.addEventListener("click", closeFilterMenuHandler);
overlay.addEventListener("click", closeFilterMenuHandler);
