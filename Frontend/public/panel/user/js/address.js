import { createAddress } from "./funcs/address.js";

const addLocationBtn = document.getElementById("add-location");

window.addEventListener("load", () => {
  addLocationBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createAddress();
  });
});
