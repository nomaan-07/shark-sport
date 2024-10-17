//// Test Fetching

const nameInputElement = document.querySelector(".name-input")
const lastnameInputElement = document.querySelector(".lastname-input")
const emailInputElement = document.querySelector(".email-input")
const passwordInputElement = document.querySelector(".password-input")
const registerBtn = document.querySelector("#register-btn")

const testFetch = () => {
  const addNewUser = {
    name : nameInputElement.value,
    lastname : lastnameInputElement.value,
    username : emailInputElement.value,
    password : passwordInputElement.value,
  }
  fetch("http://localhost:8000/user/signup" , {
    method : "POST",
    headers : {
      "Content-Type": "application/json",
      "accept": "application/json" 
    },
    body : JSON.stringify(addNewUser),
  }) 
  .then(response => {
    console.log(response)
    return response.json()
  })
  .then(data => {
    console.log(data)
  })
}

registerBtn.addEventListener("click", (e) => {
  e.preventDefault()
  testFetch()
})