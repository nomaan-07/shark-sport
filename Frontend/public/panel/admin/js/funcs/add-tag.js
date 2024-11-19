import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const labeNameInputElem = document.getElementById("labe-name");

const createTag = async () => {
  const response = await fetch(
    `http://localhost:8000/api/admin/content/tag/create`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: labeNameInputElem.value.trim(),
      }),
    }
  );
  const tags = await response.json();
  console.log(response);
  console.log(tags);
  if (response.status === 201) {
    showSwal(
      "برچسب مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {
        clearInputValue();
      }
    );
  } else if (response.status === 409) {
    showSwal(
      "تگ مورد نظر قبلا ایجاد شده است لطفا تگ دیگری را بیافزایید.",
      "error",
      "متوجه شدم.",
      () => {}
    );
  } else {
    showSwal(
      "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
      "error",
      "متوجه شدم.",
      () => {}
    );
  }
};

const clearInputValue = () => {
  labeNameInputElem.value = "";
};

export { createTag };
