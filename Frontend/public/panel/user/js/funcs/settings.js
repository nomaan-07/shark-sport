import { showSwal, getToken } from "../../../../scripts/funcs/utils.js";

const fileInputElem = document.getElementById("file-input");
const profileImageElem = document.getElementById("profile-image");
const nameInputElem = document.getElementById("name");
const lastnameInputElem = document.getElementById("lastname");
const usernameInputElem = document.getElementById("username");
const emailInputElem = document.getElementById("email");
const phoneInputElem = document.getElementById("phone");
const passwordInputElem = document.getElementById("password");

let profileCover,
  userID = null;

const getAndShowUserInfos = async () => {
  const response = await fetch("http://localhost:8000/api/user/get_me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });
  const user = await response.json();
  console.log(user);
  userID = user.auth_dict.uid;
  nameInputElem.value = user.user.name;
  lastnameInputElem.value = user.user.lastname;
  usernameInputElem.value = user.user.username;
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

const updateAdminInfos = async () => {
  const formData = new FormData();
  formData.append("avatar", profileCover);
  formData.append("name", nameInputElem.value.trim());
  formData.append("lastname", lastnameInputElem.value.trim());
  formData.append("username", usernameInputElem.value.trim());
  formData.append("email", emailInputElem.value.trim());
  formData.append("phone_number", phoneInputElem.value.trim());
  formData.append("password", passwordInputElem.value.trim());

  const response = await fetch(
    `http://localhost:8000/api/user/update/${userID}`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
      body: formData,
    }
  );
  const result = await response.json();
  console.log(response);
  console.log(result);
  if (response.status === 200) {
    showSwal(
      "اطلاعات شما با موفقیت بروزرسانی گردید.",
      "success",
      "متشکرم",
      () => {
        location.reload();
      }
    );
  } else {
    showSwal(
      "متاسفانه خطایی رخ داده است لطفا مجددا تلاش فرمایید.",
      "error",
      "متوجه شدم",
      () => {}
    );
  }
};

export { getAndShowUserInfos, prepareUploadPhoto, updateAdminInfos };
