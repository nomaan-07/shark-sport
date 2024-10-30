import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const addNewAdmin = async () => {
  const nameInputElem = document.getElementById("name");
  const lastnameInputElem = document.getElementById("lastname");
  const usernameInputElem = document.getElementById("username");
  const emailInputElem = document.getElementById("email");
  const phoneInputElem = document.getElementById("phone");
  const passwordInputElem = document.getElementById("password");
  const adminAccess = document.querySelector("#product-access");
  const newAdminInfos = {
    name: nameInputElem.value.trim(),
    lastname: lastnameInputElem.value.trim(),
    username: usernameInputElem.value.trim(),
    email: emailInputElem.value.trim(),
    phone: phoneInputElem.value.trim(),
    root_access: adminAccess.dataset.access,
    password: passwordInputElem.value.trim(),
  };

  const response = await fetch(`http://localhost:8000/api/admin/create_admin`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${getToken()}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newAdminInfos),
  });
  console.log(response);
  if (response.status === 201) {
    showSwal(
      "کاربر مورد نظر با موفقیت به ادمین ارتفا پیدا کرد.",
      "success",
      "بسیار عالی",
      () => {
        clearInputsValue(
          nameInputElem,
          lastnameInputElem,
          usernameInputElem,
          emailInputElem,
          phoneInputElem,
          passwordInputElem
        );
      }
    );
  } else if (response.status === 422) {
    showSwal(
      "لطفا سطح دسترسی ادمین را انتخاب کنید.",
      "error",
      "متوجه شدم",
      () => {}
    );
  }
};

const clearInputsValue = (
  nameInputElem,
  lastnameInputElem,
  usernameInputElem,
  emailInputElem,
  phoneInputElem,
  passwordInputElem
) => {
  nameInputElem.value = "";
  lastnameInputElem.value = "";
  usernameInputElem.value = "";
  emailInputElem.value = "";
  phoneInputElem.value = "";
  passwordInputElem.value = "";
};
cl
export { addNewAdmin };
