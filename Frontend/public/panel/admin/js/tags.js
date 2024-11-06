import { getUrlParam, addParamToURL } from "../../../scripts/funcs/utils.js";
import { getAndShowAllTags, updatePagination } from "./funcs/tags.js";

window.addParamToURL = addParamToURL;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  const currentPage = getUrlParam("page") || 1;

  getAndShowAllTags(itemsPerPage, currentPage).then(() => {
    updatePagination(itemsPerPage, currentPage);
  });
});
