import { prepareUploadPhoto, addCategory } from "./funcs/add-category.js";

window.addEventListener("load", () => {
  const addCategoryBtn = document.getElementById("add-category-btn");
  prepareUploadPhoto();
  addCategoryBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addCategory();
  });
});
