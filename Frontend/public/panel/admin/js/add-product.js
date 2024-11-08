import {
  setupUploader,
  addNewProduct,
  getTags,
  getDiscounts,
  getCategories,
} from "./funcs/add-product.js";

window.addEventListener("load", () => {
  const addProductBtn = document.getElementById("add-product");

  ////////////////////////////
  // Upload Photos
  setupUploader();
  // Get Discounts to Select From Admin
  getDiscounts();
  // Get Categories to Select From Admin
  getCategories();
  // Get Tags to Select From Admin
  getTags();
  ///////////////////////////
  addProductBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addNewProduct();
  });
});
