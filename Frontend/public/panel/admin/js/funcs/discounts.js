import {
  addParamToUrlState,
  askSwal,
  getToken,
  showSwal,
  getUrlParam,
  openModalEditor,
} from "../../../../scripts/funcs/utils.js";

const currentPage = getUrlParam("page") || 1;
const nameEditInputEl = document.getElementById("name-edit");
const discountCodeEditInputEl = document.getElementById("discount-code-edit");
const discountRateEditEl = document.getElementById("discount-rate-edit");
const expiresEditEl = document.getElementById("expires_at-edit");
const updateModalElem = document.getElementById("update-modal");
let mainDiscountID = null;

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
  if (discounts.length) {
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
                              <svg onclick="prepareUpdateDiscount('${
                                discount.id
                              }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                  <use href="#edit"></use>
                              </svg>
  
                              <!-- Delete Btn -->
                              <svg onclick="removeDiscount('${
                                discount.id
                              }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                  <use href="#trash"></use>
                              </svg>
                          </div>
                      </div>
      `
      );
    });
  } else {
    discountsWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
      <div class="bg-rose-500 p-4 rounded-xl text-lg text-center text-white dark:text-black">
          هیچ تخفیفی در حال حاضر وجود ندارد.
        </div>
    `
    );
  }
  return discounts;
};

const paginationClickHandler = (page) => {
  addParamToUrlState("page", page);
  location.reload();
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

  Array.from(Array(paginatedCount).keys()).forEach((i) => {
    i = i + 1;
    paginationWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
        <div onclick="paginationClickHandler(${i})" class="panel__pagination  ${
        Number(currentPage) === i ? "panel__pagination--active" : ""
      }">${i}</div>
      `
    );
  });
};

// InComplete =>
const removeDiscount = async (discountID) => {
  askSwal(
    "آیا مطمئن به حذف تخفیف مورد نظر خود هستید؟",
    undefined,
    "warning",
    "بله مطمئنم",
    "خیر",
    async (result) => {
      if (result.isConfirmed) {
        const response = await fetch(`http://localhost:8000//${discountID}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        });
        const mess = await response.json();
        console.log(response);
        console.log(mess);
        if (response.ok) {
          showSwal(
            "تخفیف مورد نظر شما با موفقیت حذف گردید.",
            "success",
            "متشکرم",
            () => {
              // getAndShowAllDiscounts().then(() => {
              //   updatePagination()
              // });
            }
          );
        } else {
          showSwal(
            "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
            "error",
            "متوجه شدم",
            () => {}
          );
        }
      }
    }
  );
};

const prepareFlatpickr = () => {
  flatpickr(expiresEditEl, {
    locale: "fa",
    dateFormat: "Y-m-d",
  });
};

const prepareUpdateDiscount = async (discountID) => {
  // Save Discount ID
  mainDiscountID = discountID;
  ////// Scroll to show modal visibility
  openModalEditor(updateModalElem)
  const response = await fetch(
    `http://localhost:8000/api/discount/read_discount?discount_id=${discountID}`
  );
  const discount = await response.json();
  console.log(discount);
  nameEditInputEl.value = discount.name;
  discountCodeEditInputEl.value = discount.discount_code;
  discountRateEditEl.value = discount.discount_rate;
  expiresEditEl.value = discount.expires_at.slice(0, 10);
};

// InComplete =>
const updateDiscount = async () => {
  console.log(mainDiscountID);
  const updateDiscountObj = {
    name: nameEditInputEl.value.trim(),
    discount_code: discountCodeEditInputEl.value.trim(),
    discount_rate: discountRateEditEl.value.trim(),
    expires_at: expiresEditEl.value.trim(),
  };
  const response = await fetch(
    `http://localhost:8000//?discount_id=${mainDiscountID}`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateDiscountObj),
    }
  );
  const messsage = await response.json();
  console.log(response);
  console.log(messsage);
  if (response.ok) {
    showSwal(
      "تغییرات کد تخفیف مورد نظر با موفقیت اعمال شد.",
      "success",
      "متشکرم",
      () => {
        // getAndShowAllDiscounts().then(() => {
        //   updatePagination()
        // });
      }
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

// Handle Hide Modal Editor
// modalCloseBtn.addEventListener("click", () => {
//   updateModalElem.classList.add("hidden");
//   scrollTo({
//     top: 0,
//     behavior: "smooth",
//   });
// });
//////////////////////////

export {
  getAndShowAllDiscounts,
  updatePagination,
  paginationClickHandler,
  removeDiscount,
  prepareFlatpickr,
  prepareUpdateDiscount,
  updateDiscount,
};
