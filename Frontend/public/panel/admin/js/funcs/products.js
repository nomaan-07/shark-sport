import {
  getToken,
  askSwal,
  showSwal,
} from "../../../../scripts/funcs/utils.js";

const getAndShowAllProducts = async () => {
  const productListWrapperElem = document.getElementById("product-list");
  const response = await fetch(
    `http://localhost:8000/api/product/list_products?show_sizes=true&show_specifications=true&show_tags=true&show_deleted=true&limit=1000&skip=0&desc=true`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const products = await response.json();
  productListWrapperElem.innerHTML = "";
  if (products.lenght) {
    products.forEach((product) => {
      productListWrapperElem.insertAdjacentHTML(
        "beforeend",
        `
                            <!-- Product -->
                    <div class="flex items-center justify-between flex-wrap gap-4 py-2 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Name | Price | Category | Tags | Seller -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <!-- Checkbox -->
                                <label class="relative inline-block">
                                    <input type="checkbox" class="peer absolute appearance-none w-full h-full bg-transparent cursor-pointer">
                                    <span class="size-6 flex justify-center items-center border-2 border-rose-500 peer-checked:bg-rose-500 rounded-md transition-colors"></span>
                                </label>
                                <!-- Image -->
                                <div class="size-[72px] rounded-xl overflow-hidden">
                                    <img class="size-full" src="../images/shoe-1.jpg" alt="کفش">
                                </div>
                            </div>

                            <!-- Name -->
                            <span>کفش استوک فوتبالی</span>

                            <!-- Price -->
                            <div class="flex items-center gap-0.5">
                                <div class="text-end">
                                    <div class="text-rose-500">2,000,000</div>
                                    <div class="text-sm text-rose-300 line-through font-vazir">5,000,000</div>
                                </div>
                                <span class="text-sm text-rose-500">تومان</span>
                            </div>

                            <!-- Category -->
                            <span>فوتبالی</span>

                            <!-- Tags -->
                            <span>کفش , فوتبال</span>

                            <!-- Seller -->
                            <span>مدیر سایت</span>

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
            () => {}
          );
        } else {
          showSwal(
            "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
            "error",
            "متوجه شدم",
            () => {
              getAndShowAllProducts(2, 6);
            }
          );
        }
      }
    }
  );
};

export { getAndShowAllProducts, removeProduct };
