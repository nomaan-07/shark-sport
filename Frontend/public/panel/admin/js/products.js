import { getAndShowAllProducts, removeProduct } from "./funcs/products.js";

window.removeProduct = removeProduct;
window.addEventListener("load", () => {
  getAndShowAllProducts();
});
