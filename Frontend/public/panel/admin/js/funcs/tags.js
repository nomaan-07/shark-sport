import {
  askSwal,
  getToken,
  showSwal,
  getUrlParam,
} from "../../../../scripts/funcs/utils.js";

const currentPage = getUrlParam("page") || 1;
const updateModalElem = document.getElementById("update-modal");
const modalCloseBtn = document.getElementById("modal-close-btn");
const nameEditInputEl = document.getElementById("name-edit");
let mainTagID = null;

const getAndShowAllTags = async (itemsPerPage, currentPage) => {
  const tagsListWrapperElem = document.getElementById("tags-list");
  const skip = (currentPage - 1) * itemsPerPage;
  const response = await fetch(
    `http://localhost:8000/api/tag/list_tags?limit=${itemsPerPage}&skip=${skip}`
  );
  const tags = await response.json();
  tagsListWrapperElem.innerHTML = "";
  console.log(tags);
  if (tags.length) {
    tags.forEach((tag, index) => {
      tagsListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
          <div class="flex items-center justify-between flex-wrap gap-4 py-6 px-4 border border-neutral-300 rounded-2xl">
            <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
              <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                <label class="relative inline-block">${index + 1 + skip}</label>
              </div>
              <span>${tag.name}</span>
            </div>
            <div class="flex items-center gap-2 justify-end grow">
              <svg onclick="prepareUpdateTag('${
                tag.id
              }')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                <use href="#edit"></use>
              </svg>
              <svg onclick=removeTag('${
                tag.id
              }') class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                <use href="#trash"></use>
              </svg>
            </div>
          </div>
          `
      );
    });
  } else {
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

const updatePagination = async (itemsPerPage, currentPage) => {
  const paginationWrapperElem = document.getElementById("pagination-wrapper");
  const response = await fetch(
    `http://localhost:8000/api/tag/list_tags?limit=1000&skip=0`
  );
  const tags = await response.json();
  const totalTags = tags.length;
  const paginatedCount = Math.ceil(totalTags / itemsPerPage);

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

const prepareUpdateTag = async (tagID) => {
  mainTagID = tagID;
  ////// Scroll to show modal visibility
  updateModalElem.classList.remove("hidden");
  updateModalElem.scrollIntoView({
    behavior: "smooth",
  });
  const response = await fetch(`http://localhost:8000/api/tag/get/${tagID}`);
  const tag = await response.json();
  console.log(tag);
  nameEditInputEl.value = tag.name;
};

const updateTag = async () => {
  console.log(mainTagID);
  const response = await fetch(`http://localhost:8000/${mainTagID}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify({
      name: nameEditInputEl.value.trim(),
    }),
  });
  const message = await response.json();
  console.log(response);
  console.log(message);
  if (response.ok) {
    showSwal(
      "برچسب مورد نظر شما با موفقیت بروزرسانی گردید.",
      "success",
      "متشکرم",
      () => {
        // getAndShowAllTags().then(() => {
        //   updatePagination();
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

const removeTag = async (tagID) => {
  askSwal(
    "آیا مطمئن به حذف برچسب مورد نظر خود هستید؟",
    undefined,
    "warning",
    "بله مطمئنم",
    "خیر",
    async (result) => {
      if (result.isConfirmed) {
        const response = await fetch(`http://localhost:8000//${tagID}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        });
        const message = await response.json();
        console.log(response);
        console.log(message);
        if (response.ok) {
          showSwal(
            "برچسب مورد نظر شما با موفقیت حذف گردید.",
            "success",
            "متشکرم",
            () => {
              getAndShowAllTags(10, currentPage).then(() => {
                updatePagination(10, currentPage);
              });
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

// Handle Hide Modal Editor
modalCloseBtn.addEventListener("click", () => {
  updateModalElem.classList.add("hidden");
  scrollTo({
    top: 0,
    behavior: "smooth",
  });
});
//////////////////////////

export {
  getAndShowAllTags,
  updatePagination,
  prepareUpdateTag,
  updateTag,
  removeTag,
};
