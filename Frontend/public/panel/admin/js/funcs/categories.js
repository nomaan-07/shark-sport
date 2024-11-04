import {
  askSwal,
  getToken,
  showSwal,
} from "../../../../scripts/funcs/utils.js";

const getAndShowAllCategories = async (pageNumber, limit) => {
  const categoriesListWrapperElem = document.getElementById("categories-list");
  const skip = (pageNumber - 1) * limit;
  const response = await fetch(
    `http://localhost:8000/api/category/list?index=false&skip=${skip}&limit=${limit}`
  );
  const categories = await response.json();
  console.log(categories);
  categoriesListWrapperElem.innerHTML = "";
  categories.forEach((category) => {
    categoriesListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
       <div class="flex items-center justify-between flex-wrap gap-4 py-2 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Username | Email | Phone | Role -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <!-- Checkbox -->
                                <label class="relative inline-block">
                                    <input type="checkbox" class="peer absolute appearance-none w-full h-full bg-transparent cursor-pointer">
                                    <span class="size-6 flex justify-center items-center border-2 border-rose-500 peer-checked:bg-rose-500 rounded-md transition-colors"></span>
                                </label>
                                <!-- Image -->
                                <div class="size-[72px] rounded-xl overflow-hidden">
                                    <img class="size-full object-cover" src="${category.image_url}" alt="${category.name}">
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
                            <svg onclick="updateCategory('${category.id}')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#edit"></use>
                            </svg>

                            <!-- Delete Btn -->
                            <svg onclick="removeCategory('${category.id}')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                    </div>
    `
    );
  });
  return categories;
};

const removeCategory = async (categoryID) => {
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
              getAndShowAllCategories(1, 10);
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

export { getAndShowAllCategories, removeCategory, updateCategory };
