import { askSwal } from "../../../scripts/funcs/utils.js";
import {
  getAndShowUserInfos,
  prepareUploadPhoto,
  updateAdminInfos,
} from "./funcs/settings.js";

const imageUploadBtn = document.querySelector(".image-upload-btn");
const imageUploadInput = document.querySelector(".image-upload-input");
const updateUserBtn = document.getElementById("update-user-btn");
imageUploadBtn.addEventListener("click", () => imageUploadInput.click());

window.addEventListener("load", () => {
  getAndShowUserInfos();
  prepareUploadPhoto();
  updateUserBtn.addEventListener("click", (e) => {
    e.preventDefault();
    askSwal(
      "آیا از تغییرات خود مطمئن هستید؟",
      "با ثبت تغییرات تمام اطلاعات شما بروزرسانی می گردد.",
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
