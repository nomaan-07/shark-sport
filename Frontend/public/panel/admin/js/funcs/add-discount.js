import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const nameInputElem = document.getElementById("name");
const discountCodeInputElem = document.getElementById("discount-code");
const discountRateInputElem = document.getElementById("discount-rate");
const expiresAtInputElem = document.getElementById("expires_at");

const prepareFlatpickr = () => {
  flatpickr(expiresAtInputElem, {
    locale: "fa",
    dateFormat: "Y-m-d",
  });
};

const createDiscount = async () => {
  const createNewDiscount = {
    name: nameInputElem.value.trim(),
    discount_code: discountCodeInputElem.value.trim(),
    discount_rate: discountRateInputElem.value.trim(),
    expires_at: expiresAtInputElem.value.trim(),
  };

  const response = await fetch(
    "http://localhost:8000/api/admin/content/discount/create_discount",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(createNewDiscount),
    }
  );
  const discounts = await response.json();
  console.log(response);
  console.log(discounts);
  if (response.ok) {
    showSwal(
      "تخفیف مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {}
    );
  } else {
    showSwal(
      "متاسفانه خطایی رخ داده است مجددا تلاش فرمایید.",
      "error",
      "متوجه شدم",
      () => {}
    );
  }
};

export { prepareFlatpickr, createDiscount };
