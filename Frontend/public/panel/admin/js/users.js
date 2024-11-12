import {
  getUrlParam,
  showToast,
  addParamToUrlState,
} from "../../../scripts/funcs/utils.js";
import { updatePagination } from "./funcs/users.js";
import {
  getAndShowAllUsers,
  paginationClickHandler,
  removeUser,
} from "./funcs/users.js";

window.paginationClickHandler = paginationClickHandler;
window.removeUser = removeUser;
window.addEventListener("load", () => {
  const itemsPerPage = 10;
  let currentPage = getUrlParam("page") || 1;
  let urlisShowAdmins = getUrlParam("isShowAdmins");
  let urlisShowUsers = getUrlParam("isShowUsers");
  let isShowAdmins = urlisShowAdmins === "true";
  let isShowUsers = urlisShowUsers === "true";
  if (!isShowAdmins && !isShowUsers) {
    isShowAdmins = true;
    isShowUsers = true;
  }
  const filterShowParameters = document.querySelectorAll(
    ".panel-filter__option"
  );

  getAndShowAllUsers(itemsPerPage, currentPage, isShowAdmins, isShowUsers).then(
    () => {
      updatePagination(itemsPerPage, currentPage, isShowAdmins, isShowUsers);
    }
  );

  // Select Filter Users
  filterShowParameters.forEach((filterShowParameter) => {
    filterShowParameter.setAttribute(
      "selected",
      filterShowParameter.dataset.filter
    );
    filterShowParameter.addEventListener("click", (e) => {
      if (e.target.dataset.filter === "all") {
        getAndShowAllUsers(itemsPerPage, currentPage, true, true).then(() => {
          updatePagination(itemsPerPage, currentPage, true, true);
        });
      } else if (e.target.dataset.filter === "admins") {
        addParamToUrlState("isShowAdmins", filterShowParameter.dataset.user);
        getAndShowAllUsers(itemsPerPage, currentPage, true, false).then(() => {
          updatePagination(itemsPerPage, currentPage, true, false);
        });
      } else if (e.target.dataset.filter === "users") {
        addParamToUrlState("isShowUsers", filterShowParameter.dataset.user);
        getAndShowAllUsers(itemsPerPage, currentPage, false, true).then(() => {
          updatePagination(itemsPerPage, currentPage, false, true);
        });
      } else {
        showToast("top-end", 3000, "warning", "لطفا یک گزینه را انتخاب کنید.");
      }
    });
  });
});
