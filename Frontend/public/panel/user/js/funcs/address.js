import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const stateInputEl = document.getElementById("state");
const cityInputEl = document.getElementById("city");
const streetAddressInputEl = document.getElementById("street-address");
const reciverPhoneInputEl = document.getElementById("reciver-phone");
const reciverFullnameInputEl = document.getElementById("reciver-fullname");
const postalCodeInputEl = document.getElementById("postal-code");

const createAddress = async () => {
  const addAddress = {
    street_address: streetAddressInputEl.value.trim(),
    city: cityInputEl.value.trim(),
    state: stateInputEl.value.trim(),
    postal_code: postalCodeInputEl.value.trim(),
    reciver_phone: reciverPhoneInputEl.value.trim(),
    reciver_fullname: reciverFullnameInputEl.value.trim(),
  };
  const response = await fetch(
    "http://localhost:8000/api/user/address/create",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(addAddress),
    }
  );
  const address = await response.json();
  console.log(response);
  console.log(address);
  if (response.ok) {
    showSwal(
      "آدرس مورد نظر با موفقیت اضافه گردید.",
      "success",
      "متشکرم",
      () => {
        clearInputsValue();
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

const clearInputsValue = () => {
  stateInputEl.value = "";
  cityInputEl.value = "";
  streetAddressInputEl.value = "";
  reciverPhoneInputEl.value = "";
  reciverFullnameInputEl.value = "";
  postalCodeInputEl.value = "";
};

export { createAddress };
