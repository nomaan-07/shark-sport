import {
  saveIntoLocalStorage,
  getFromLocalStorage,
  showToast,
} from "../../../scripts/funcs/utils.js";

window.addEventListener("load", () => {});

// Show Welcome Alert Message
if (!getFromLocalStorage("toastShown")) {
  showToast("top-end", 3000, "success", "به پنل مدیریتی خود خوش آمدید.");
}
saveIntoLocalStorage("toastShown", "true");
