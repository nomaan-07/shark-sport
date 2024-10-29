import {
  prepareCreateNewProduct,
  addNewProduct,
} from "./funcs/add-products.js";

window.addEventListener("load", () => {
  const addProductBtn = document.getElementById("add-product");

  prepareCreateNewProduct();

  addProductBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addNewProduct();
  });
});
