import { prepareFlatpickr, createDiscount } from "./funcs/add-discount.js";

window.addEventListener("load", () => {
  const addDiscountBtn = document.getElementById("add-discount-btn");
  addDiscountBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createDiscount();
  });
  // Prepare Date Discount
  prepareFlatpickr();
});
