import {
  getAndShowAllCategories,
  getAndShowAllProducts,
  getAndShowAllSuggestions,
  getAndShowAllDiscounts,
} from "./funcs/index.js";

window.addEventListener("load", () => {
  getAndShowAllCategories();
  getAndShowAllProducts();
  getAndShowAllSuggestions();
  getAndShowAllDiscounts();
});
