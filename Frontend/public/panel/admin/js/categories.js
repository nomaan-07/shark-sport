import { addParamToURL, getUrlParam } from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllCategories,
  updatePagination,
  removeCategory,
  updateCategory,
} from "./funcs/categories.js";

window.addParamToURL = addParamToURL;
window.removeCategory = removeCategory;
window.updateCategory = updateCategory;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;

  getAndShowAllCategories(itemsPerPage, currentPage).then(() => {
    updatePagination(itemsPerPage, currentPage);
  });
});
