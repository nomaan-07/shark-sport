import { askSwal, showSwal } from "../../../scripts/funcs/utils.js";
import {
  updateAdminInfos,
  prepareUploadPhoto,
  getAndShowAdminInfos,
} from "./funcs/settings.js";

window.addEventListener("load", () => {
  const updateInfosBtn = document.getElementById("update-infos-btn");
  getAndShowAdminInfos();
  prepareUploadPhoto();

  updateInfosBtn.addEventListener("click", (e) => {
    e.preventDefault();
    askSwal(
      "آیا از تغییرات خود مطمئن هستید؟",
      undefined,
      "warning",
      "بله مطمئنم",
      "خیر",
      async (result) => {
        if (result.isConfirmed) {
          updateAdminInfos();
        }
      }
    );
  });
});
