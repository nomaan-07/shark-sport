import {
  getToken,
  showSwal,
  showToast,
} from "../../../../scripts/funcs/utils.js";

const profileImageElem = document.getElementById("profile-image");
const fileInputElem = document.getElementById("file-input");
const categoryNameElem = document.getElementById("category-name");
const categoryLinkElem = document.getElementById("category-link");
let profileCover = null;

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

const addCategory = async () => {
  const formData = new FormData();
  formData.append("image", profileCover);
  formData.append("name", categoryNameElem.value.trim());
  formData.append("description", categoryLinkElem.value.trim());
  const response = await fetch(
    `http://localhost:8000/api/admin/content/create_category`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
      body: formData,
    }
  );
  const category = await response.json();
  console.log(response);
  console.log(category);
  if (response.status === 409) {
    showSwal(
      "این دسته بندی در حال حاضر موجود است.",
      "error",
      "متوجه شدم",
      () => {}
    );
  } else if (response.status === 200) {
    showSwal(
      "دسته بندی مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {
        clearInputsValue();
      }
    );
  } else if (response.status === 422) {
    showSwal(
      "لینک دسته بندی باید کمتر از 300 کاراکتر باشد.",
      "error",
      "متوجه شدم",
      () => {}
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

const clearInputsValue = () => {
  profileImageElem.src = "../../images/category/category-10.png";
  categoryNameElem.value = "";
  categoryLinkElem.value = "";
};

export { prepareUploadPhoto, addCategory };
