import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const profileImageElem = document.getElementById("profile-image");
const fileInputElem = document.getElementById("file-input");
const categoryNameElem = document.getElementById("category-name");
const categoryDescriptionElem = document.getElementById("category-description");
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
  formData.append("description", categoryDescriptionElem.value.trim());
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
  if (response.status === 200) {
    showSwal(
      "دسته بندی مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {
        clearInputsValue();
      }
    );
  }
};

const clearInputsValue = () => {
  profileImageElem.src = "../../images/category/category-10.png";
  categoryNameElem.value = "";
  categoryDescriptionElem.value = "";
};

export { prepareUploadPhoto, addCategory };
