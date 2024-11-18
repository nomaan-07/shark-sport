import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

const notifModalEl = document.getElementById("notif-modal");

const getNotifications = async () => {
  const notifCounterEl = document.getElementById("notif-counter");
  const response = await fetch(
    `http://localhost:8000/api/notification/list?read=false&index=false&limit=1000&skip=0`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );
  const notifications = await response.json();
  console.log(notifications)
  if (notifications.count > 9) {
    notifCounterEl.innerHTML = "9+";
  } else {
    notifCounterEl.innerHTML = notifications.count;
  }
  notifModalEl.innerHTML = "";
  if (notifications.count) {
    notifications.notifications.forEach((notification, index) => {
      notifModalEl.insertAdjacentHTML(
        "beforeend",
        `
        <div class="flex-between py-2.5">
          <span>${index + 1}</span>
          <span onclick="detailsNotification('${
            notification.id
          }')" class="truncate w-[190px]">${notification.subject}</span>
          <span onclick="seenNotification('${notification.id}')">دیدم</span>
        </div>
      `
      );
    });
  } else {
    notifModalEl.insertAdjacentHTML(
      "beforeend",
      `
      <div">در حال حاضر هیچ اعلانی وجود ندارد.</div>
    `
    );
  }
  console.log(notifications);
};

const detailsNotification = async (notificationID) => {
  const response = await fetch(
    `http://localhost:8000/api/notificationall_users/get/${notificationID}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );
  const detailNotification = await response.json();

  Swal.fire({
    title: detailNotification.subject,
    text: detailNotification.message,
    confirmButtonText: "مشاهده کردم",
  }).then((result) => getNotifications());

  console.log(detailNotification);
};

const seenNotification = async (notificationID) => {
  const response = await fetch(
    `http://localhost:8000/api/notificationall_users/get/${notificationID}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );
  getNotifications();
};

const showNotifications = () => {
  notifModalEl.classList.remove("hidden");
};

const hideNotifications = () => {
  notifModalEl.classList.add("hidden");
};

export {
  getNotifications,
  showNotifications,
  hideNotifications,
  detailsNotification,
  seenNotification,
};
