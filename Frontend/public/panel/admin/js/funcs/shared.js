import { getToken } from "../../../../scripts/funcs/utils.js";

const getNotifications = async () => {
  const response = await fetch(
    `http://localhost:8000/api/notification/admin/get/list?limit=100&skip=0&index=false`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );
  const message = await response.json();
  console.log(response);
  console.log(message);
};

const showNotifications = () => {
  console.log("show");
};

const hideNotifications = () => {
  console.log("hide");
};

export { getNotifications, showNotifications, hideNotifications };
