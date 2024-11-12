import {
  showToast,
  getUrlParam,
  addParamToURL,
  addParamToUrlState,
  askSwal,
  closeModalEditor,
} from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllDiscounts,
  paginationClickHandler,
  prepareUpdateDiscount,
  updatePagination,
  removeDiscount,
  updateDiscount,
  prepareFlatpickr,
} from "./funcs/discounts.js";

// Binding Functions
window.prepareUpdateDiscount = prepareUpdateDiscount;
window.updateDiscount = updateDiscount;
window.removeDiscount = removeDiscount;
window.paginationClickHandler = paginationClickHandler;
// Binding Functions

window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;
  let urlIsExpired = getUrlParam("isExpired");
  let isExpired = !urlIsExpired ? false : true;
  const filterShowParameters = document.querySelectorAll(
    ".panel-filter__option"
  );
  const updateDiscountBtn = document.getElementById("add-discount-btn");
  //////////////////////////////
  const updateModalElem = document.getElementById("update-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  closeModalEditor(modalCloseBtn, updateModalElem);
  //////////////////////////////
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
  // Prepare Date Discount
  prepareFlatpickr();
  // Edit & Show Last Changes Data
  updateDiscountBtn.addEventListener("click", (e) => {
    e.preventDefault();
    askSwal(
      "آیا مطمئن به بروزرسانی تخفیف مورد نظر خود هستید؟",
      "بعد از دکمه ثبت تمام تغییرات اعمال می شود.",
      "warning",
      "بله مطمئنم",
      "خیر",
      (result) => {
        if (result.isConfirmed) {
          updateDiscount();
        }
      }
    );
  });
  ////
});
