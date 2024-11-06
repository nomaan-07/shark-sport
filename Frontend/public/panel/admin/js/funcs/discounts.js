import {
  addParamToURL,
  formatNumber,
  getUrlParam,
} from "../../../../scripts/funcs/utils.js";

const getAndShowAllDiscounts = async (itemsPerPage, currentPage, isExpired) => {
  const discountsWrapperElem = document.getElementById("discounts-list");
  const skip = (currentPage - 1) * itemsPerPage;
  const response = await fetch(
    `http://localhost:8000/api/discount/list_discounts?limit=${itemsPerPage}&skip=${skip}&expired=${isExpired}&index=false`
  );
  const discounts = await response.json();
  console.log(response);
  console.log(discounts);
  discountsWrapperElem.innerHTML = "";
  discounts.forEach((discount, index) => {
    discountsWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
            <div class="flex items-center justify-between flex-wrap gap-4 py-6 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Username | Email | Phone | Role -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <label class="relative inline-block">${
                                  index + 1 + skip
                                }</label>
                            </div>
                            <!-- Name -->
                            <span>${discount.name}</span>
                            <!-- Rate -->
                            <span>${discount.discount_rate}%</span>
                            <!--  -->
                            <span>${discount.discount_code}</span>
                            <!--  -->
                            <span>${discount.expires_at.slice(0, 10)}</span>
                        </div>

                        <!-- Buttons: Edit Btn | Delete Btn-->
                        <div class="flex items-center gap-2 justify-end grow">
                            <!-- Edit Btn -->
                            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#edit"></use>
                            </svg>

                            <!-- Delete Btn -->
                            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                    </div>
    `
    );
  });
  return discounts;
};

const updatePagination = async (itemsPerPage, currentPage, isExpired) => {
  const response = await fetch(
    `http://localhost:8000/api/discount/list_discounts?limit=1000&skip=0&expired=${isExpired}&index=false`
  );
  const discounts = await response.json();
  const totalDiscounts = discounts.length;
  const paginatedCount = Math.ceil(totalDiscounts / itemsPerPage);
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

export { getAndShowAllDiscounts, updatePagination };
