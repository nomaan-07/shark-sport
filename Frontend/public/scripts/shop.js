// import noUiSlider from '../../node_modules/nouislider/dist/nouislider.mjs'
import { toggleSelect, selectOption } from "./ui/ui-handlers.js";
import { overlay } from "./shared/header-footer.js";
import {
  overlayVisible,
  overlayHidden,
  mobileMenuVisible,
  mobileMenuHidden,
  formatNumber,
} from "./funcs/shared.js";
// Price Slider Element
const priceSliderElements = document.querySelectorAll(".price-slider");
const priceSliderValues = document.querySelectorAll(".price-slider-value");
// Filtration elements of products
const selectElementsHeaders = document.querySelectorAll(
  ".panel-select__header"
);
// Filter Menu Mobile Elements
const openfilterBtn = document.getElementById("filter-btn");
const closeFilterBtn = document.getElementById("close-filter-btn");
const mobileMenuFilter = document.querySelector(".mobile-menu-filter");

priceSliderElements.forEach((sliderElem) => {
  noUiSlider.create(sliderElem, {
    start: [0, 10000000],
    connect: true,
    range: {
      min: 0,
      max: 10000000,
    },
    step: 100000,
  });

  sliderElem.noUiSlider.on("update", (values) => {
    const formattedMin = formatNumber(Math.round(values[0]));
    const formattedMax = formatNumber(Math.round(values[1]));
    const prices = [formattedMax, formattedMin];
    priceSliderValues.forEach((value, index) => {
      value.innerHTML = `${prices[index % 2]} تومان`
    })
  });
});

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

const openFilterMenuHandler = () => {
  mobileMenuVisible(mobileMenuFilter, "-right-[300px]", "right-0");
  overlayVisible(overlay, "overlay--visible");
};

const closeFilterMenuHandler = () => {
  mobileMenuHidden(mobileMenuFilter, "-right-[300px]", "right-0");
  overlayHidden(overlay, "overlay--visible");
};

selectElementsHeaders.forEach((el) => handleSelect(el));
openfilterBtn.addEventListener("click", openFilterMenuHandler);
closeFilterBtn.addEventListener("click", closeFilterMenuHandler);
overlay.addEventListener("click", closeFilterMenuHandler);
