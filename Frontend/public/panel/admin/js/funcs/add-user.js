import {
  getToken,
  showSwal,
  showToast,
} from "../../../../scripts/funcs/utils.js";

// Elements From DOM
const nameInputElem = document.getElementById("name");
const lastnameInputElem = document.getElementById("lastname");
const usernameInputElem = document.getElementById("username");
const emailInputElem = document.getElementById("email");
const phoneInputElem = document.getElementById("phone");
const passwordInputElem = document.getElementById("password");
const adminAccess = document.querySelector("#product-access");
const profileImageElem = document.getElementById("profile-image");
const fileInputElem = document.getElementById("file-input");

let profileCover,
  nameValid,
  lastNameValid,
  userNameValid,
  emailValid,
  phoneValid,
  passwordValid = null;

const isNameValid = () => {
  const nameInputElem = document.getElementById("name");
  const nameRegex = /^[\u0600-\u06FF\s]{3,30}$/;
  nameInputElem.addEventListener("blur", () => {
    if (!nameRegex.test(nameInputElem.value.trim())) {
      showToast(
        "top-end",
        3000,
        "error",
        "نام باید به زبان فارسی و حداقل 3 کاراکتر داشته باشد."
      );
      nameValid = false;
    } else {
      nameValid = true;
    }
  });
};

const isLastNameValid = () => {
  const lastnameInputElem = document.getElementById("lastname");
  const lastNameRegex = /^[\u0600-\u06FF\s]{3,30}$/;
  lastnameInputElem.addEventListener("blur", () => {
    if (!lastNameRegex.test(lastnameInputElem.value.trim())) {
      showToast(
        "top-end",
        3000,
        "error",
        "نام خانوادگی باید به زبان فارسی و حداقل 3 کاراکتر داشته باشد."
      );
      lastNameValid = false;
    } else {
      lastNameValid = true;
    }
  });
};

const isUserNameValid = () => {
  const usernameInputElem = document.getElementById("username");
  const userNameRegex = /^[a-zA-Z0-9._-]{3,30}$/;
  usernameInputElem.addEventListener("blur", () => {
    if (!userNameRegex.test(usernameInputElem.value.trim())) {
      showToast(
        "top-end",
        3000,
        "error",
        "نام کاربری باید حداقل شامل 3 کاراکتر باشد."
      );
      userNameValid = false;
    } else {
      userNameValid = true;
    }
  });
};

const isEmailValid = () => {
  const emailInputElem = document.getElementById("email");
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  emailInputElem.addEventListener("blur", () => {
    if (!emailRegex.test(emailInputElem.value.trim())) {
      showToast("top-end", 3000, "error", "ایمیل وارد شده معتبر نمی باشد.");
      emailValid = false;
    } else {
      emailValid = true;
    }
  });
};

const isPhoneValid = () => {
  const phoneInputElem = document.getElementById("phone");
  const phoneRegex = /^(09\d{9}|989\d{9})$/;
  phoneInputElem.addEventListener("blur", () => {
    if (!phoneRegex.test(phoneInputElem.value.trim())) {
      showToast("top-end", 3000, "error", "شماره تماس وارد شده صحیح نمی باشد.");
      phoneValid = false;
    } else {
      phoneValid = true;
    }
  });
};

const isPasswordValid = () => {
  const passwordInputElem = document.getElementById("password");
  const phoneRegex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$])[A-Za-z\d@#$]{8,}$/;
  passwordInputElem.addEventListener("blur", () => {
    if (!phoneRegex.test(passwordInputElem.value.trim())) {
      showToast(
        "top-end",
        3000,
        "error",
        "رمز عبور باید حداقل 8 کاراکتر و شامل حداقل یک حرف بزرگ و یک حرف کوچک و اشکال &#@ باشد."
      );
      passwordValid = false;
    } else {
      passwordValid = true;
    }
  });
};

const prepareUploadPhoto = () => {
  fileInputElem.addEventListener("change", (e) => {
    const file = e.target.files[0];
    profileCover = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        profileImageElem.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
};

const addNewAdmin = async () => {
  const formData = new FormData();
  formData.append("name", nameInputElem.value.trim());
  formData.append("lastname", lastnameInputElem.value.trim());
  formData.append("username", usernameInputElem.value.trim());
  formData.append("email", emailInputElem.value.trim());
  formData.append("phone", phoneInputElem.value.trim());
  formData.append("root_access", adminAccess.dataset.access);
  formData.append("password", passwordInputElem.value.trim());
  formData.append("avatar", profileCover);

  if (
    (nameValid,
    lastNameValid,
    userNameValid,
    emailValid,
    phoneValid,
    passwordValid)
  ) {
    const response = await fetch(
      `http://localhost:8000/api/admin/create_admin`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${getToken()}`,
        },
        body: formData,
      }
    );
    const result = await response.json();
    console.log(result);
    console.log(response);
    if (response.status === 201) {
      console.log(profileCover);
      showSwal(
        "کاربر مورد نظر با موفقیت به ادمین ارتفا پیدا کرد.",
        "success",
        "بسیار عالی",
        () => {
          clearInputsValue();
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
  } else {
    showToast(
      "top-end",
      3000,
      "error",
      "متاسفانه شما موارد ضروری فیلد ها را رعایت نکردید."
    );
  }
};

const clearInputsValue = () => {
  profileImageElem.src = "../images/avatar-2.jpg";
  fileInputElem.value = "";
  nameInputElem.value = "";
  lastnameInputElem.value = "";
  usernameInputElem.value = "";
  emailInputElem.value = "";
  phoneInputElem.value = "";
  passwordInputElem.value = "";
};

export {
  addNewAdmin,
  isNameValid,
  isLastNameValid,
  isUserNameValid,
  isEmailValid,
  isPhoneValid,
  isPasswordValid,
  prepareUploadPhoto,
};
