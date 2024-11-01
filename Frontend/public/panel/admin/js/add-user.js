import { showSwal } from "../../../scripts/funcs/utils.js";
import { addNewAdmin } from "./funcs/add-user.js";
import { getMe } from "./funcs/login.js";

window.addEventListener("load", () => {
  const addAdminBtn = document.getElementById("add-admin-btn");
  //   Check If User has access (for add new admin)
  getMe().then((adminInfos) => {
    if (!adminInfos.auth_dict.root_access) {
      showSwal(
        "شما به این بخش از پنل ادمین دسترسی ندارد.",
        "error",
        "متوجه شدم",
        () => {
          location.href = "index.html";
        }
      );
    }
  });
  addAdminBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addNewAdmin();
  });
});
