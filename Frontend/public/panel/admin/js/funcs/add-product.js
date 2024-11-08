import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const nameInputElem = document.getElementById("name");
const descriptionInputElem = document.getElementById("description");
const originalPriceInputElem = document.getElementById("original-price");
const productCategoryElem = document.getElementById("product-category");
const surveyInputElem = document.getElementById("survey");
const warrantyInputElem = document.getElementById("warranty");
const productDiscountInputElem = document.getElementById("product-discount");
const productTagInputElem = document.getElementById("product-tag");
const brandInputElem = document.getElementById("brand");
const sizesInputElem = document.getElementById("sizes");
const colorsInputElem = document.getElementById("colors");
const qtysInputElem = document.getElementById("qtys");
const specificationNamesInputElem = document.getElementById(
  "specification-names"
);
const specificationDescriptionsInputElem = document.getElementById(
  "specification-descriptions"
);

let imageSources = [null, null, null];
let discountID,
  categoryID,
  tagID = null;

const setupUploader = () => {
  const currentImages = document.querySelectorAll(".current-image");
  const imageUploaders = document.querySelectorAll(".image-uploader");
  imageUploaders.forEach((imageUploader, index) => {
    imageUploader.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          currentImages[index].src = e.target.result;
          imageSources[index] = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  });
};

const getDiscounts = async () => {
  const discountListWrapperElem = document.getElementById("discount-list");
  const response = await fetch(
    `http://localhost:8000/api/discount/list_discounts?limit=100&skip=0&expired=false&index=false`
  );
  const discounts = await response.json();
  console.log(discounts);
  if (discounts.length) {
    discounts.forEach((discount) => {
      discountListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
        <p class="panel__option panel__option--category" data-category="${discount.id}">${discount.name}</p>
      `
      );
    });
  } else {
    discountListWrapperElem.innerHTML = "";
    discountListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
        <div class="bg-rose-500 p-4 rounded-xl text-lg text-center text-white dark:text-black">
          هیچ تخفیفی در حال حاضر وجود ندارد.
        </div>
    `
    );
  }
};

const getTags = async () => {
  const tagsListWrapperElem = document.getElementById("tags-list");
  const response = await fetch(
    "http://localhost:8000/api/tag/list_tags?limit=100&skip=0",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const tags = await response.json();
  console.log(tags.length);
  if (tags.length) {
    tags.forEach((tag) => {
      tagsListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
        <p class="panel__option panel__option--tag" data-tag="${tag.id}">${tag.name}</p>
      `
      );
    });
  } else {
    tagsListWrapperElem.innerHTML = "";
    tagsListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
       <div class="bg-rose-500 p-4 rounded-xl text-lg text-center text-white dark:text-black">
          هیچ برچسبی در حال حاضر وجود ندارد.
        </div>
    `
    );
  }
  return tags;
};

const getCategories = async () => {
  const categoriesListWrapperElem = document.getElementById("categories-list");
  const response = await fetch(
    `http://localhost:8000/api/category/list?index=false&skip=0&limit=100`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const categories = await response.json();
  if (categories.length) {
    categories.forEach((category) => {
      categoriesListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
        <p class="panel__option panel__option--category" data-category="${category.id}">${category.name}</p>
      `
      );
    });
  } else {
    categoriesListWrapperElem.innerHTML = "";
    categoriesListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
       <div class="bg-rose-500 p-4 rounded-xl text-lg text-center text-white dark:text-black">
          هیچ دسته بندی در حال حاضر وجود ندارد.
        </div>
    `
    );
  }

  console.log(productCategoryElem.dataset.category);
  categoryID = productCategoryElem.dataset.category;
};

const addNewProduct = async () => {
  console.log("test");
  const formData = new FormData();
  formData.append("images", imageSources);
  formData.append("tag", tagID);
  formData.append("discount_id", discountID);
  formData.append("category_id", categoryID);
  formData.append("name", nameInputElem.value.trim());
  formData.append("description", descriptionInputElem.value.trim());
  formData.append("survey", surveyInputElem.value.trim());
  formData.append("original_price", originalPriceInputElem.value.trim());
  formData.append("warranty", warrantyInputElem.value.trim());
  formData.append("brand", brandInputElem.value.trim());
  formData.append("sizes", sizesInputElem.value.trim());
  formData.append("colors", colorsInputElem.value.trim());
  formData.append("qtys", qtysInputElem.value.trim());
  formData.append(
    "specification_names",
    specificationNamesInputElem.value.trim()
  );
  formData.append(
    "specification_descriptions",
    specificationDescriptionsInputElem.value.trim()
  );
  const response = await fetch(
    `http://localhost:8000/api/admin/content/create_product`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
      body: formData,
    }
  );
  if (response.ok) {
    showSwal(
      "محصول مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {}
    );
  } else {
    showSwal(
      "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
      "error",
      "متوجه شدم",
      () => {}
    );
  }
};

export { setupUploader, addNewProduct, getTags, getDiscounts, getCategories };
