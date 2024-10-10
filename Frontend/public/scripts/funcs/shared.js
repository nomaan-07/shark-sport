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

export { overlayVisible, overlayHidden, mobileMenuVisible, mobileMenuHidden };
