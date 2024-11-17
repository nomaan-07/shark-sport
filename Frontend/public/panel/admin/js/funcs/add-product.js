import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";
import { handleSelectOptions } from "../../../js/ui/ui-handlers.js";

const nameInputElem = document.getElementById("name");
const descriptionInputElem = document.getElementById("description");
const originalPriceInputElem = document.getElementById("original-price");
const surveyInputElem = document.getElementById("survey");
const warrantyInputElem = document.getElementById("warranty");
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
// Elements From DOM For Getting IDs
const productTagID = document.getElementById("product-tag");
const productDiscountID = document.getElementById("product-discount");
const productCategoryID = document.getElementById("product-category");

const imageSources = [null, null, null];

const setupUploader = () => {
  const currentImages = document.querySelectorAll(".current-image");
  const imageUploaders = document.querySelectorAll(".image-uploader");
  imageUploaders.forEach((imageUploader, index) => {
    imageUploader.addEventListener("change", (e) => {
      const file = e.target.files[0];
      imageSources[index] = e.target.files[0];
      console.log(imageSources);
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          currentImages[index].src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  });
};

const getDiscounts = async (type) => {
  const discountListWrapperElem = document.getElementById("discounts-list");
  const response = await fetch(
    `http://localhost:8000/api/discount/list_discounts?limit=100&skip=0&expired=false&index=false`
  );
  const discounts = await response.json();
  console.log(discounts);
  if (discounts.length) {
    discountListWrapperElem.innerHTML = `<p class="panel__option panel__option--discount" data-discount="null">تخفیف ها</p>`;
    discounts.forEach((discount) => {
      discountListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
        <p class="panel__option panel__option--discount" data-discount="${discount.id}">
          <span>${discount.name}</span>
          <span>${discount.discount_rate}%</span>
        </p>
      `
      );
    });
    // Add event listeners to newly created elements
    handleSelectOptions(type);
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

const getTags = async (type) => {
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
  if (tags.length) {
    tagsListWrapperElem.innerHTML = `<p class="panel__option panel__option--tag" data-tag="null">تگ ها</p>`;
    tags.forEach((tag) => {
      tagsListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
          <p class="panel__option panel__option--tag" data-tag="${tag.id}">${tag.name}</p>
        `
      );
    });
    // Add event listeners to newly created elements
    handleSelectOptions(type);
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

const getCategories = async (type) => {
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
    categoriesListWrapperElem.innerHTML = `<p class="panel__option panel__option--category" data-category="null">دسته بندی ها</p>`;
    categories.forEach((category) => {
      categoriesListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
        <p class="panel__option panel__option--category" data-category="${category.id}">${category.name}</p>
      `
      );
    });
    // Add event listeners to newly created elements
    handleSelectOptions(type);
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
};

const addNewProduct = async () => {
  const formData = new FormData();
  imageSources.forEach((imageSource) => {
    if (imageSource) {
      formData.append("images", imageSource);
    }
  });
  formData.append("name", nameInputElem.value.trim());
  formData.append("description", descriptionInputElem.value.trim());
  formData.append("survey", surveyInputElem.value.trim());
  formData.append("original_price", originalPriceInputElem.value.trim());
  formData.append("warranty", warrantyInputElem.value.trim());
  formData.append("discount_id", productDiscountID.dataset.discount);
  formData.append("category_id", productCategoryID.dataset.category);
  formData.append("tag_id", productTagID.dataset.tag);
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

  console.log(`متحویات فرم دیتا : `);
  for (const [key, value] of formData.entries()) {
    console.log(key, value);
  }

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
  const mess = await response.json();
  console.log(response);
  console.log(mess);
  if (response.status === 201) {
    showSwal(
      "محصول مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {}
    );
  } else if (response.status === 409) {
    showSwal(
      "محصول انتخابی قبلا با این عنوان ثبت شده است.",
      "error",
      "متوجه شدم",
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
