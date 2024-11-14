const categoryWrapperElem = document.getElementById("category-wrapper");

const getAndShowAllCategories = async () => {
  const response = await fetch(
    "http://localhost:8000/api/category/list/?index=false&skip=0&limit=100"
  );
  const categories = await response.json();
  const categoriesShuffledArray = categories.sort(() => 0.5 - Math.random());
  categoryWrapperElem.innerHTML = "";
  categoriesShuffledArray.slice(0, 12).forEach((category) => {
    categoryWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
            <div class="category-box flex-center flex-col gap-y-1">
                <a href="shop.html?category=${category.description}" class="relative size-24 sm:size-[140px] bg-orangeTint_1 rounded-full">
                    <img class="absolute right-0 left-0 m-auto -top-5 size-[85%]" src="${category.image_url}" alt="${category.name}">
                </a>
                <span class="text-base xs:text-lg sm:text-xl xl:text-2xl font-vazirMedium">${category.name}</span>
            </div>
        `
    );
  });
};

export { getAndShowAllCategories };
