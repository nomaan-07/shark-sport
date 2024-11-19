const getAndShowAllCategories = async () => {
  const categoryWrapperElem = document.getElementById("category-wrapper");
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

const getAndShowAllProducts = async () => {
  const productsWrapperStories = document.getElementById(
    "products-wrapper-stories"
  );
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=false&show_specifications=false&show_tags=false&show_deleted=false&limit=1000&skip=0&desc=false`
  );
  const products = await response.json();
  productsWrapperStories.innerHTML = "";
  const produstsShuffledArray = products.sort(() => 0.5 - Math.random());
  produstsShuffledArray.forEach((product) => {
    productsWrapperStories.insertAdjacentHTML(
      "beforeend",
      `
      <div class="swiper-slide">
        <div class="stories__item flex-center relative overflow-hidden size-[100px] sm:size-[130px] rounded-[50%]">
          <a href="#">
            <img class="stories__img relative size-[90px] sm:size-[115px] object-cover z-10 rounded-[50%]" src="${product.images[0]}" alt="sport-equ-1" loading="lazy">
          </a>
        </div>
      </div>
    `
    );
  });
};

const getAndShowAllSuggestions = async () => {
  const productSuggestionsWrapper = document.getElementById(
    "product-suggestions-wrapper"
  );
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=false&show_specifications=false&show_tags=false&show_deleted=false&limit=1000&skip=0&desc=false`
  );
  const products = await response.json();
  const produstsShuffledArray = products.sort(() => 0.5 - Math.random());
  productSuggestionsWrapper.innerHTML = "";
  produstsShuffledArray.forEach((product) => {
    productSuggestionsWrapper.insertAdjacentHTML(
      "beforeend",
      `
        <div class="swiper-slide">
          <div class="home-product__box flex flex-col relative font-vazirBold h-[326px] pb-7 bg-white overflow-hidden text-lg">
              <span class="flex-center absolute left-1.5 top-1.5 text-orangeBrand bg-orangeTint_1 w-14 h-8 rounded-full">${
                100 -
                (product.price_after_discount / product.original_price) * 100
              }%</span>
              <a class="flex-center m-auto w-[150px] h-[55%]" href="#">
                  <img class="size-full" src="${product.images[0]}" alt="">
              </a>
              <h4 class="text-center mb-2.5">${product.name}</h4>
              <div class="home-product__price flex-center gap-x-2">
                  <div class="flex-center flex-col gap-y-1">
                      <span>${product.price_after_discount.toLocaleString()}</span>
                      <span class="text-grayTint_4">${product.original_price.toLocaleString()}</span>
                  </div>
                  <span class="text-base">تومان</span>
              </div>
          </div>
        </div>
    `
    );
  });
  console.log(products);
};

const getAndShowAllDiscounts = async () => {
  const productDiscountsWrapper = document.getElementById(
    "product-discount-wrapper"
  );
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=false&show_specifications=false&show_tags=false&show_deleted=false&limit=1000&skip=0&desc=false`
  );
  const products = await response.json();
  const produstsShuffledArray = products.sort(() => 0.5 - Math.random());
  productDiscountsWrapper.innerHTML = "";
  produstsShuffledArray.forEach((product) => {
    productDiscountsWrapper.insertAdjacentHTML(
      "beforeend",
      `
        <div class="swiper-slide">
          <div class="home-product__box flex flex-col relative font-vazirBold h-[326px] pb-7 bg-white overflow-hidden text-lg">
              <span class="flex-center absolute left-1.5 top-1.5 text-orangeBrand bg-orangeTint_1 w-14 h-8 rounded-full">${
                100 -
                (product.price_after_discount / product.original_price) * 100
              }%</span>
              <a class="flex-center m-auto w-[150px] h-[55%]" href="#">
                  <img class="size-full" src="${product.images[0]}" alt="">
              </a>
              <h4 class="text-center mb-2.5">${product.name}</h4>
              <div class="home-product__price flex-center gap-x-2">
                  <div class="flex-center flex-col gap-y-1">
                      <span>${product.price_after_discount.toLocaleString()}</span>
                      <span class="text-grayTint_4">${product.original_price.toLocaleString()}</span>
                  </div>
                  <span class="text-base">تومان</span>
              </div>
          </div>
        </div>
    `
    );
  });
  console.log(products);
};

export {
  getAndShowAllCategories,
  getAndShowAllProducts,
  getAndShowAllSuggestions,
  getAndShowAllDiscounts,
};
