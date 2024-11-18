import { getUrlParam } from "../../../../scripts/funcs/utils.js";
import {
  getToken,
  askSwal,
  showSwal,
} from "../../../../scripts/funcs/utils.js";

const currentPage = getUrlParam("page") || 1;

const getAndShowAllProducts = async (itemsPerPage, currentPage) => {
  const skip = (currentPage - 1) * itemsPerPage;
  const productListWrapperElem = document.getElementById("product-list");
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=false&show_specifications=false&show_tags=true&show_deleted=false&limit=${itemsPerPage}&skip=${skip}&desc=false`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const products = await response.json();
  console.log(products);
  productListWrapperElem.innerHTML = "";
  if (products.length) {
    products.forEach((product, index) => {
      productListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
                            <!-- Product -->
                    <div class="flex items-center justify-between flex-wrap gap-4 py-2 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Name | Price | Category | Tags | Seller -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <label class="relative inline-block">${
                                  index + 1
                                }</label>
                                <!-- Image -->
                                <div class="size-[72px] rounded-xl overflow-hidden">
                                    <img class="size-full" src="${
                                      product.images[0]
                                    }" alt="${product.name}" loading="lazy">
                                </div>
                            </div>

                            <!-- Name -->
                            <span>${product.name}</span>

                            <!-- Price -->
                            <div class="flex items-center gap-0.5">
                                <div class="text-end">
                                    <div class="text-rose-500">${product.price_after_discount.toLocaleString()}</div>
                                    <div class="text-sm text-rose-300 line-through font-vazir">${product.original_price.toLocaleString()}</div>
                                </div>
                                <span class="text-sm text-rose-500">تومان</span>
                            </div>

                            <!-- Brand -->
                            <span>${product.brand}</span>

                            <!-- Tags -->
                            <span>${product.tags}</span>

                            <!-- Warranty -->
                            <span>${product.warranty}</span>

                        </div>

                        <!-- Buttons: Edit Btn | Delete Btn-->
                        <div class="flex items-center gap-2 justify-end grow">
                            <!-- Delete Btn -->
                            <svg onclick="removeProduct('${
                              product.id
                            }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                    </div>
      `
      );
    });
  } else if (products.detail === "No products found") {
    productListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
        <div class="bg-rose-500 p-4 rounded-xl text-lg text-center text-white dark:text-black">
          هیچ محصولی در حال حاضر وجود ندارد.
        </div>
    `
    );
  }
  console.log(products);
};

const updatePagination = async (itemsPerPage, currentPage) => {
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=false&show_specifications=false&show_tags=false&show_deleted=false&limit=1000&skip=0&desc=false`
  );
  const categories = await response.json();
  const totalCategories = categories.length;
  const paginatedCount = Math.ceil(totalCategories / itemsPerPage);
  const paginationWrapperElem = document.getElementById("pagination-wrapper");
  paginationWrapperElem.innerHTML = "";

  for (let i = 1; i <= paginatedCount; i++) {
    paginationWrapperElem.insertAdjacentHTML(
      "beforeend",

      `
      ${
        Number(currentPage) === i
          ? `
        <div onclick="addParamToURL('page' , ${i})" class="panel__pagination panel__pagination--active">${i}</div>
      `
          : `
        <div onclick="addParamToURL('page' , ${i})" class="panel__pagination">${i}</div>
       `
      }
      `
    );
  }
};

const removeProduct = async (productId) => {
  console.log(productId);
  askSwal(
    "آیا مطمئن به حذف محصول مورد نظر خود هستید؟",
    undefined,
    "warning",
    "بله مطمئنم",
    "خیر",
    async (result) => {
      if (result.isConfirmed) {
        const response = await fetch(
          `http://localhost:8000/api/admin/content/products/${productId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${getToken()}`,
              "Content-Type": "application/json",
            },
          }
        );
        if (response.ok) {
          showSwal(
            "محصول مورد نظر با موفقیت حذف گردید.",
            "success",
            "متشکرم",
            () => {
              getAndShowAllProducts(10, currentPage);
            }
          );
        } else {
          showSwal(
            "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
            "error",
            "متوجه شدم",
            () => {
              getAndShowAllProducts(10, currentPage);
            }
          );
        }
      }
    }
  );
};

export { getAndShowAllProducts, updatePagination, removeProduct };
