import { toggleSelect, selectOption } from "./ui/ui-handlers.js";
import { overlay } from "./shared/header-footer.js";
import {
  overlayVisible,
  overlayHidden,
  mobileMenuVisible,
  mobileMenuHidden,
} from "./funcs/shared.js";
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
