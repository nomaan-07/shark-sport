import {
  askSwal,
  removeFromLocalStorage,
  showSwal,
  showToast,
} from "../../../../scripts/funcs/utils.js";
import { getMe } from "../funcs/login.js";
import { logout } from "../../../js/utils/utils.js";
import {
  getNotifications,
  showNotifications,
  hideNotifications,
} from "../funcs/shared.js";

window.addEventListener("load", () => {
  const adminNameElem = document.getElementById("admin-name");
  const adminUsernameElem = document.getElementById("admin-username");
  const adminImageProfileElem = document.getElementById("admin-image-profile");
  const logoutBtnElem = document.getElementById("logout-btn");
  const notificationBtn = document.querySelector("#notification-btn");
  const sharkSportSiteEl = document.getElementById("shark-sport-site");
  getMe().then((adminInfo) => {
    console.log(adminInfo);
    adminNameElem.innerHTML = `${adminInfo.admin.name} ${adminInfo.admin.lastname}`;
    adminUsernameElem.innerHTML = adminInfo.admin.username;
    adminImageProfileElem.src = adminInfo.admin.avatar_url;
  });

  logoutBtnElem.addEventListener("click", () => {
    askSwal(
      "آیا مطمئن به خروج از اکانت مدیریتی خود هستید؟",
      undefined,
      "warning",
      "بله مطمئنم",
      "خیر",
      (result) => {
        if (result.isConfirmed) {
          showSwal(
            "شما با موفقیت از اکانت مدیریتی خود خارج شدید.",
            "success",
            "متشکرم",
            () => {
              logout();
              location.href = "login.html";
              removeFromLocalStorage("toastShown");
            }
          );
        }
      }
    );
  });

  sharkSportSiteEl.addEventListener("click", () => {
    showToast("top-end" , 3000 , "error" , "برای ورود به سایت از سمت پنل ادمین نمی توانید وارد شوید.")
  })


  getNotifications();

  notificationBtn.addEventListener("mouseenter", () => {
    showNotifications();
  });

  notificationBtn.addEventListener("mouseleave", () => {
    hideNotifications();
  });
});
