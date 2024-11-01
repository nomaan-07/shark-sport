import { getMe } from "../../../scripts/funcs/auth.js";
import { askSwal, showSwal } from "../../../scripts/funcs/utils.js";
import { logout } from "../../js/utils/utils.js";

window.addEventListener("load", () => {
  const userFullNameElem = document.getElementById("user-fullname");
  const userUsernameElem = document.getElementById("user-username");
  const logoutBtnElem = document.getElementById("logout-btn");
  //   User Infos Handler
  getMe().then((userInfos) => {
    console.log(userInfos);
    userFullNameElem.innerHTML = `${userInfos.user.name} ${userInfos.user.lastname}`;
    userUsernameElem.innerHTML = userInfos.user.username;
  });

  logoutBtnElem.addEventListener("click", () => {
    askSwal(
      "آیا برای خروج از اکانت خود مطمئن هستید؟",
      undefined,
      "warning",
      "بله مطمئنم",
      "خیر",
      (result) => {
        if (result.isConfirmed) {
          showSwal(
            "شما با موفقیت از اکانت  کاربری خود خارج شدید.",
            "success",
            "متشکرم",
            () => {
              logout();
              location.href = "../../index.html";
            }
          );
        }
      }
    );
  });
});
