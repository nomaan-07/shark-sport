import { getUrlParam } from "./utils.js";

const productTitleEl = document.querySelector("#product-title");
const productDescriptionEl = document.getElementById("product-description");
const productSurveyEl = document.getElementById("product-survey");
const productOriginalPriceEl = document.getElementById(
  "product-original-price"
);
const productPriceDiscountEl = document.getElementById(
  "product-price-after-discount"
);
const productPercentEl = document.getElementById("product-percent");
const productwarrantyEl = document.getElementById("product-warranty");
const productBrandEl = document.getElementById("product-brand");
const productPublishEl = document.getElementById("product-publish");

const getAndShowSingleProduct = async () => {
  const productID = getUrlParam("id");
  const response = await fetch(
    `http://localhost:8000/api/product/products/${productID}`
  );
  const product = await response.json();
  ////// Infos
  console.log(product);
  productTitleEl.textContent = product.name;
  productDescriptionEl.textContent = product.description;
  productSurveyEl.textContent = product.survey;
  productOriginalPriceEl.textContent = product.original_price.toLocaleString();
  productPriceDiscountEl.textContent =
    product.price_after_discount.toLocaleString();
  productPercentEl.textContent = `% ${
    100 - (product.price_after_discount / product.original_price) * 100
  }`;
  productwarrantyEl.textContent = `گارانتی :  ${product.warranty}`;
  productBrandEl.textContent = `برند :  ${product.brand}`;
  productPublishEl.textContent = product.created_at.slice(0, 4);
};

const getAndShowDetailProduct = async () => {};

const handleNavBarTitles = () => {
  const navBarItem = document.querySelectorAll(".dividing-line__nav li");
  navBarItem.forEach((item) => {
    item.addEventListener("click", (e) => {
      // Scroll To The Target
      const targetID = item.getAttribute("data-target");
      const targetPart = document.getElementById(targetID);
      targetPart.scrollIntoView({
        behavior: "smooth",
      });
      // Add & Remove Active Class
      navBarItem.forEach((item) =>
        item.classList.remove("product-nav__item--active")
      );
      e.target.classList.add("product-nav__item--active");
    });
  });
};

export { getAndShowSingleProduct, getAndShowDetailProduct, handleNavBarTitles };
