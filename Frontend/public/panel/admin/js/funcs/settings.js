import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";
import { getMe } from "../funcs/login.js";

const fileInputElem = document.getElementById("file-input");
const profileImageElem = document.getElementById("profile-image");
const nameInputElem = document.getElementById("name");
const lastnameInputElem = document.getElementById("lastname");
const usernameInputElem = document.getElementById("username");
const passwordInputElem = document.getElementById("password");
const emailInputElem = document.getElementById("email");
const phoneInputElem = document.getElementById("phone");

let profileCover,
  rootAccess = null;

const getAndShowAdminInfos = () => {
  getMe().then((adminInfos) => {
    profileImageElem.src = adminInfos.admin.avatar_url;
    nameInputElem.value = adminInfos.admin.name;
    lastnameInputElem.value = adminInfos.admin.lastname;
    usernameInputElem.value = adminInfos.admin.username;
    emailInputElem.value = adminInfos.admin.email;
    phoneInputElem.value = adminInfos.admin.phone;
    rootAccess = adminInfos.auth_dict.root_access;
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

const updateAdminInfos = async () => {
  const formData = new FormData();
  formData.append("avatar", profileCover);
  formData.append("name", nameInputElem.value.trim());
  formData.append("lastname", lastnameInputElem.value.trim());
  formData.append("username", usernameInputElem.value.trim());
  formData.append("password", passwordInputElem.value.trim());
  formData.append("email", emailInputElem.value.trim());
  formData.append("phone", phoneInputElem.value.trim());
  //    No Needed These Props
  formData.append("root_access", rootAccess);
  formData.append("google_analyze_website", true);
  formData.append("google_analytics_token", "google_analytics_token");
  formData.append("instagram_token", "instagram_token");
  console.log(formData);

  const response = await fetch("http://localhost:8000/api/admin/update", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
    body: formData,
  });
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

export { updateAdminInfos, prepareUploadPhoto, getAndShowAdminInfos };
