import { showSwal } from "../../../scripts/funcs/utils.js";
import {
  addNewAdmin,
  isNameValid,
  isLastNameValid,
  isUserNameValid,
  isEmailValid,
  isPhoneValid,
  isPasswordValid,
  prepareUploadPhoto,
} from "./funcs/add-user.js";
import { getMe } from "./funcs/login.js";

window.addEventListener("load", () => {
  const addAdminBtn = document.getElementById("add-admin-btn");

  isNameValid();
  isLastNameValid();
  isUserNameValid();
  isEmailValid();
  isPhoneValid();
  isPasswordValid();
  prepareUploadPhoto();

  addAdminBtn.addEventListener("click", (e) => {
    e.preventDefault();
    addNewAdmin();
  });

  //   Check If Admin has access (for add new admin)
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
});
