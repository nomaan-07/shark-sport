import { getUrlParam } from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllProducts,
  removeProduct,
  updatePagination,
} from "./funcs/products.js";

window.removeProduct = removeProduct;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;
  getAndShowAllProducts(itemsPerPage, currentPage).then(() => {
    updatePagination(itemsPerPage, currentPage);
  });
});
