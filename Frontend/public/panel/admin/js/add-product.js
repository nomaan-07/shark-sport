import {
  setupUploader,
  addNewProduct,
  getTags,
  getDiscounts,
  getCategories,
} from "./funcs/add-products.js";

window.addEventListener("load", () => {
  const addProductBtn = document.getElementById("add-product");

  setupUploader();
  // getTags();
  getDiscounts();
  getCategories();
  addProductBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addNewProduct();
  });
});
