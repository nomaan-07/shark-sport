import {
  getAndShowAllCategories,
  removeCategory,
  updateCategory,
} from "./funcs/categories.js";

window.removeCategory = removeCategory;
window.updateCategory = updateCategory;
window.addEventListener("load", () => {
  getAndShowAllCategories(1, 10);
});
