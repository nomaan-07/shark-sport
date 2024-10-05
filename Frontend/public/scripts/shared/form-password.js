const passwordInput = document.getElementById("password-input");
const displayPasswordBtn = document.getElementById("display-password-btn");
const form = document.querySelector("form");

const showEyeSvg = (e) => {
  if (e.target.id === "password-input") {
    setTimeout(() => displayPasswordBtn.classList.remove("hide"), 400);
  }
};

const hideEyeSvg = () => {
  if (!passwordInput.value) {
    if (passwordInput.id === "password-input") {
      displayPasswordBtn.classList.add("hide");
    }
  }
};

const showPassword = () => {
  displayPasswordBtn.children[0].classList.add("hidden");
  displayPasswordBtn.children[1].classList.remove("hidden");
  passwordInput.type = "text";
};
const hidePassword = () => {
  displayPasswordBtn.children[0].classList.remove("hidden");
  displayPasswordBtn.children[1].classList.add("hidden");
  passwordInput.type = "password";
};

const displayPasswordHandler = () => {
  passwordInput.type === "password" ? showPassword() : hidePassword();
};

form.addEventListener("click", (e) => showEyeSvg(e));
passwordInput.addEventListener("blur", hideEyeSvg);
displayPasswordBtn.addEventListener("click", displayPasswordHandler);