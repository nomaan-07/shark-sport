import {
  getAndShowSingleProduct,
  getAndShowDetailProduct,
  handleNavBarTitles,
} from "./funcs/single-product.js";

window.addEventListener("load", () => {
  getAndShowSingleProduct();
  getAndShowDetailProduct();
  handleNavBarTitles();
});
