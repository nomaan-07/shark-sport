import { login } from "./funcs/login.js";

window.addEventListener("load", () => {
  const loginBtn = document.getElementById("login-btn");
  loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    login();
  });
});
