import {
  addParamToURL,
  askSwal,
  getUrlParam,
} from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllCategories,
  updatePagination,
  removeCategory,
  prepareUploadPhoto,
  prepareUpdateCategory,
  updateCategory,
} from "./funcs/categories.js";

window.addParamToURL = addParamToURL;
window.removeCategory = removeCategory;
window.prepareUpdateCategory = prepareUpdateCategory;
window.updateCategory = updateCategory;

window.addEventListener("load", () => {
  const updateCategoryBtn = document.getElementById("update-category-btn");
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;

  // Show Categories
  getAndShowAllCategories(itemsPerPage, currentPage).then(() => {
    updatePagination(itemsPerPage, currentPage);
  });

  // Upload Photo Category
  prepareUploadPhoto();

  // Edit & Show Last Changes Data
  updateCategoryBtn.addEventListener("click", (e) => {
    e.preventDefault();
    askSwal(
      "آیا مطمئن به بروزرسانی دسته بندی مورد نظر خود هستید؟",
      "بعد از دکمه ثبت تمام تغییرات اعمال می شود.",
      "warning",
      "بله مطمئنم",
      "خیر",
      (result) => {
        if (result.isConfirmed) {
          updateCategory();
        }
      }
    );
  });
  ////
});
