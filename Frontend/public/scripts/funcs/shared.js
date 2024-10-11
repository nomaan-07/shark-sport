const overlayVisible = (overlay, visibleClass) =>
  overlay.classList.add(visibleClass);

const overlayHidden = (overlay, visibleClass) =>
  overlay.classList.remove(visibleClass);

const mobileMenuVisible = (menu, hideClass, visibleClass) => {
  menu.classList.remove(hideClass);
  menu.classList.add(visibleClass);
};

const mobileMenuHidden = (menu, hideClass, visibleClass) => {
  menu.classList.add(hideClass);
  menu.classList.remove(visibleClass);
};

const updateSlider = (priceValue, rangevalue, rangeInputvalue) => {
  let minp = parseInt(priceValue[0].value);
  let maxp = parseInt(priceValue[1].value);

  rangevalue.style.right = `${(minp / rangeInputvalue[0].max) * 100}%`;
  rangevalue.style.left = `${100 - (maxp / rangeInputvalue[1].max) * 100}%`;
};

export {
  overlayVisible,
  overlayHidden,
  mobileMenuVisible,
  mobileMenuHidden,
  updateSlider,
};
