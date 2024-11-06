import {
  askSwal,
  getToken,
  getUrlParam,
  showSwal,
} from "../../../../scripts/funcs/utils.js";

const getAndShowAllCategories = async (itemsPerPage, currentPage) => {
  const categoriesListWrapperElem = document.getElementById("categories-list");
  const skip = (currentPage - 1) * itemsPerPage;
  const response = await fetch(
    `http://localhost:8000/api/category/list?index=false&skip=${skip}&limit=${itemsPerPage}`
  );
  const categories = await response.json();
  console.log(categories);
  categoriesListWrapperElem.innerHTML = "";
  categories.forEach((category, index) => {
    categoriesListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
       <div class="flex items-center justify-between flex-wrap gap-4 py-2 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Username | Email | Phone | Role -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <label class="relative inline-block">${
                                  index + 1 + skip
                                }</label>
                                <!-- Image -->
                                <div class="size-[72px] rounded-xl overflow-hidden">
                                    <img class="size-full object-cover" src="${
                                      category.image_url
                                    }" alt="${category.name}">
                                </div>
                            </div>
                            <!-- Name -->
                            <span>${category.name}</span>
                            <!-- Description -->
                            <span>${category.description}</span>
                        </div>

                        <!-- Buttons: Edit Btn | Delete Btn-->
                        <div class="flex items-center gap-2 justify-end grow">
                            <!-- Edit Btn -->
                            <svg onclick="updateCategory('${
                              category.id
                            }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#edit"></use>
                            </svg>

                            <!-- Delete Btn -->
                            <svg onclick="removeCategory('${
                              category.id
                            }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                    </div>
    `
    );
  });
  return categories;
};

const updatePagination = async (itemsPerPage, currentPage) => {
  const response = await fetch(
    `http://localhost:8000/api/category/list?index=false&skip=0&limit=1000`
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

const removeCategory = async (categoryID) => {
  const currentPage = getUrlParam("page") || 1;
  askSwal(
    "آیا مطمئن به حذف دسته بندی مورد نظر هستید؟",
    undefined,
    "warning",
    "بله مطمئنم",
    "خیر",
    async (result) => {
      if (result.isConfirmed) {
        const response = await fetch(
          `http://localhost:8000/api/category/delete/${categoryID}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${getToken()}`,
              "Content-Type": "application/json",
            },
          }
        );
        console.log(response);
        if (response.ok) {
          showSwal(
            "دسته بندی مورد نظر به موفقیت حذف گردید.",
            "success",
            "متشکرم",
            () => {
              getAndShowAllCategories(10, currentPage);
            }
          );
        } else {
          showSwal(
            "متاسفانه خطایی رخ داده است مجددا تلاش فرمایید.",
            "error",
            "متوجه شدم",
            () => {}
          );
        }
      }
    }
  );
};

const updateCategory = async (categoryID) => {
  console.log(categoryID);
};

export {
  getAndShowAllCategories,
  updatePagination,
  removeCategory,
  updateCategory,
};
