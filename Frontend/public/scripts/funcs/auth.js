import {
  getToken,
  saveIntoLocalStorage,
  showSwal,
} from "../../scripts/funcs/utils.js";

const register = async () => {
  const nameInputElem = document.querySelector(".name");
  const lastnameInputElem = document.querySelector(".lastname");
  const usernameInputElem = document.querySelector(".username");
  const passwordInputElem = document.querySelector(".password");
  const newUserInfos = {
    name: nameInputElem.value.trim(),
    lastname: lastnameInputElem.value.trim(),
    username: usernameInputElem.value.trim(),
    password: passwordInputElem.value.trim(),
  };
  const response = await fetch(`http://localhost:8000/api/user/Auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newUserInfos),
  });
  const result = await response.json();
  if (response.status === 201) {
    showSwal("ثبت نام شما با موفقیت انجام شد.", "success", "متشکرم", () => {
      location.href = "login.html";
      clearInputsRegister(
        nameInputElem,
        lastnameInputElem,
        usernameInputElem,
        passwordInputElem
      );
    });
  } else if (response.status === 409) {
    showSwal(
      "ایمیل یا تلفن همراه قبلا ثبت نام کرده است.",
      "error",
      "تصحیح اطلاعات",
      () => {}
    );
  } else if (response.status === 422) {
    showSwal(
      "متاسفانه خطایی در فرایند ثبت نام شما رخ داده است، مجددا تلاش فرمایید.",
      "error",
      "بسیار خب",
      () => {}
    );
  }
  console.log(response);
  console.log(result);
};

const login = async () => {
  const usernameInputElem = document.querySelector(".username");
  const passwordInputElem = document.querySelector(".password");
  const data = new URLSearchParams();
  data.append("username", usernameInputElem.value.trim());
  data.append("password", passwordInputElem.value.trim());

  const response = await fetch(`http://localhost:8000/api/user/Auth/login`, {
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
  }
  console.log(response);
  console.log(result);
};

const getMe = async () => {
  const token = getToken();
  if (!token) {
    return false;
  }
  const response = await fetch("http://localhost:8000/api/user/get_me", {
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

export { register, login, getMe };
