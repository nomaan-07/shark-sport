
const response = await fetch("http://localhost:8000/user/signup/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json", // Correct header for JSON
        "Accept": "application/json" // Adding accept header
    },
    body:JSON.stringify({
      name: "اسم تستی",
      lastname : "فامیل تستی",
      username : "یوزر تستی",
      password : "1234",
      })
  })
  const data = await response.json();
  return data 

console.log(getMeInfoFromBack())
//