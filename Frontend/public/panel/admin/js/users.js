import { showToast } from "../../../scripts/funcs/utils.js";
import { getAndShowAllUsers, removeUser } from "./funcs/users.js";

window.removeUser = removeUser;
window.addEventListener("load", () => {
  const filterShowParameters = document.querySelectorAll(
    ".panel-filter__option"
  );
  // Select Filter Users
  getAndShowAllUsers(true, true, 1, 10);
  filterShowParameters.forEach((filterShowParameter) => {
    filterShowParameter.addEventListener("click", (e) => {
      if (e.target.dataset.filter === "all") {
        getAndShowAllUsers(true, true, 1, 10);
      } else if (e.target.dataset.filter === "admins") {
        getAndShowAllUsers(true, false, 1, 10);
      } else if (e.target.dataset.filter === "users") {
        getAndShowAllUsers(false, true, 1, 10);
      } else {
        showToast("top-end", 3000, "warning", "لطفا یک گزینه را انتخاب کنید.");
      }
    });
  });
});
