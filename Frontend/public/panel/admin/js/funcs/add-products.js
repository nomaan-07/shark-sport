const nameInputElem = document.getElementById("name");
const descriptionInputElem = document.getElementById("description");
const originalPriceInputElem = document.getElementById("original-price");
const productCategoryElem = document.getElementById("product-category");
let imageSources = [null, null, null];
let discountID,
  categoryID = null;

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

const getTags = async () => {
  const response = await fetch(
    "http://localhost:8000/api/tag/list_tags?limit=10&skip=0",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const tags = await response.json();
  console.log(tags);
};

const getDiscounts = async () => {
  const response = await fetch(
    `http://localhost:8000/api/discount/list_discounts?limit=100&skip=0&expired=true&index=false`
  );
  const discounts = await response.json();
  // console.log(discounts)
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
  console.log(categories);
  categories.forEach((category) => {
    categoriesListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
      <p class="panel__option panel__option--category" data-category="${category.name}">${category.name}</p>
    `
    );
  });

  console.log(productCategoryElem.dataset.category);
  categoryID = productCategoryElem.dataset.category;
};

const addNewProduct = () => {
  console.log("test");
  const formData = new FormData();
  formData.append("images", imageSources);
  formData.append("name", nameInputElem.value.trim());
  formData.append("description", descriptionInputElem.value.trim());
  // formData.append("survey",)
  formData.append("original_price", originalPriceInputElem.value.trim());
  // formData.append("warranty",)
  // formData.append("discount_id",)
  // formData.append("category_id",)
  // formData.append("brand",)
  // formData.append("sizes",)
  // formData.append("colors",)
  // formData.append("qtys",)
  // formData.append("specification_names",)
  // formData.append("specification_descriptions",)
  // formData.append("tags",)
};

export { setupUploader, addNewProduct, getTags, getDiscounts, getCategories };
