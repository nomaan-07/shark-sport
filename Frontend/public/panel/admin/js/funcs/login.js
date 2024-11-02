import {
  showSwal,
  saveIntoLocalStorage,
  getToken,
} from "../../../../scripts/funcs/utils.js";

const login = async () => {
  const usernameInputElem = document.querySelector(".username");
  const passwordInputElem = document.querySelector(".password");
  const data = new URLSearchParams();
  data.append("username", usernameInputElem.value.trim());
  data.append("password", passwordInputElem.value.trim());

  const response = await fetch(`http://localhost:8000/api/admin/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: data.toString(),
  });
  const result = await response.json();

  if (response.status === 200) {
    showSwal("ورود شما با موفقیت انجام شد.", "success", "ورود به سایت", () => {
      saveIntoLocalStorage("user", { token: result.access_token });
      saveIntoLocalStorage("refresh", { token: result.refresh_token });
      location.href = "index.html";
      clearInputsRegister(
        usernameInputElem,
        passwordInputElem,
        usernameInputElem,
        passwordInputElem
      );
    });
  } else if (response.status === 422) {
    showSwal(
      "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
      "error",
      "متوجه شدم.",
      () => {}
    );
  } else if (response.status === 400) {
    showSwal(
      "نام کاربری یا رمز عبور معتبر نمی باشد.",
      "error",
      "متوجه شدم.",
      () => {}
    );
  }
  console.log(response);
  console.log(result);
};

const getMe = async () => {
  const token = getToken();
  if (!token) {
    return false;
  }
  const response = await fetch("http://localhost:8000/api/admin/get_me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  return data;
};

const clearInputsRegister = (name, lastname, username, password) => {
  name.value = "";
  lastname.value = "";
  username.value = "";
  password.value = "";
};

export { login, getMe };
