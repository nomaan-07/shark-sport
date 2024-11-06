import {
  showToast,
  getUrlParam,
  addParamToURL,
} from "../../../scripts/funcs/utils.js";
import { getAndShowAllDiscounts, updatePagination } from "./funcs/discounts.js";

window.addParamToURL = addParamToURL;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;
  const filterShowParameters = document.querySelectorAll(
    ".panel-filter__option"
  );

  getAndShowAllDiscounts(itemsPerPage, currentPage, false).then(() =>
    updatePagination(itemsPerPage, currentPage, false)
  );

  // Select Filter Users
  filterShowParameters.forEach((filterShowParameter) => {
    filterShowParameter.addEventListener("click", (e) => {
      if (e.target.dataset.filter === "expired") {
        e.target.dataset.filter = false;
        getAndShowAllDiscounts(itemsPerPage, currentPage, true).then(() =>
          updatePagination(itemsPerPage, currentPage, true)
        );
      } else if (e.target.dataset.filter === "authentic") {
        getAndShowAllDiscounts(itemsPerPage, currentPage, false).then(() =>
          updatePagination(itemsPerPage, currentPage, false)
        );
      } else {
        showToast(
          "top-end",
          3000,
          "warning",
          "لطفا یک گزینه را انتخاب نمایید."
        );
      }
    });
  });
});
