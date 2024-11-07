import {
  showToast,
  getUrlParam,
  addParamToURL,
  addParamToUrlState,
} from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllDiscounts,
  paginationClickHandler,
  updatePagination,
} from "./funcs/discounts.js";

window.paginationClickHandler = paginationClickHandler;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;
  let urlIsExpired = getUrlParam("isExpired");
  let isExpired = !urlIsExpired ? false : true;
  const filterShowParameters = document.querySelectorAll(
    ".panel-filter__option"
  );

  getAndShowAllDiscounts(itemsPerPage, currentPage, isExpired).then(() =>
    updatePagination(itemsPerPage, currentPage, isExpired)
  );

  // Select Filter Discounts
  filterShowParameters.forEach((filterShowParameter) => {
    filterShowParameter.setAttribute(
      "selected",
      filterShowParameter.dataset.filter
    );

    filterShowParameter.addEventListener("click", (e) => {
      addParamToUrlState("isExpired", filterShowParameter.dataset.expired);
      if (e.target.dataset.filter === "expired") {
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
