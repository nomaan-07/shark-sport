import { register } from "./funcs/auth.js";

window.addEventListener("load", () => {
  const registerBtn = document.getElementById("register-btn");
  registerBtn.addEventListener("click", (e) => {
    e.preventDefault();
    register();
  });
});
