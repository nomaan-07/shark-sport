import { login } from "./funcs/auth.js";
import { showToast } from "./funcs/utils.js";

window.addEventListener("load", () => {
  showToast("top-end", 3000, "info", "اطلاعات خود را وارد نمایید.");
  const loginBtn = document.querySelector("#login-btn");
  loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    login();
  });
});
