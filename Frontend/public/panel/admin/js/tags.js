import { getUrlParam, addParamToURL, askSwal } from "../../../scripts/funcs/utils.js";
import {
  getAndShowAllTags,
  updatePagination,
  prepareUpdateTag,
  updateTag,
  removeTag,
} from "./funcs/tags.js";

window.prepareUpdateTag = prepareUpdateTag;
window.updateTag = updateTag;
window.removeTag = removeTag;
window.addParamToURL = addParamToURL;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  const currentPage = getUrlParam("page") || 1;
  const updateTagBtn = document.getElementById("add-tag-btn");

  getAndShowAllTags(itemsPerPage, currentPage).then(() => {
    updatePagination(itemsPerPage, currentPage);
  });

  // Edit & Show Last Changes Data
  updateTagBtn.addEventListener("click", (e) => {
    e.preventDefault();
    askSwal(
      "آیا مطمئن به بروزرسانی برچسب مورد نظر خود هستید؟",
      "بعد از دکمه ثبت تمام تغییرات اعمال می شود.",
      "warning",
      "بله مطمئنم",
      "خیر",
      (result) => {
        if (result.isConfirmed) {
          updateTag();
        }
      }
    );
  });
  ////
});
