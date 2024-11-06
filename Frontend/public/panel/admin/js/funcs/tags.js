const getAndShowAllTags = async (itemsPerPage, currentPage) => {
  const tagsListWrapperElem = document.getElementById("tags-list");
  const skip = (currentPage - 1) * itemsPerPage;
  const response = await fetch(
    `http://localhost:8000/api/tag/list_tags?limit=${itemsPerPage}&skip=${skip}`
  );
  const tags = await response.json();
  tagsListWrapperElem.innerHTML = "";
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
            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
              <use href="#edit"></use>
            </svg>
            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
              <use href="#trash"></use>
            </svg>
          </div>
        </div>
        `
    );
  });
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

export { getAndShowAllTags, updatePagination };
