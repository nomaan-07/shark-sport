import {
  askSwal,
  getToken,
  showSwal,
} from "../../../../scripts/funcs/utils.js";

const getAndShowAllUsers = async (showAdmins, showUsers, pageNumber, limit) => {
  const usersListWrapperElem = document.getElementById("users-list");
  const skip = (pageNumber - 1) * limit;
  const response = await fetch(
    `http://localhost:8000/api/admin/user-management/list_all?admins=${showAdmins}&users=${showUsers}&index=false&limit=${limit}&skip=${skip}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "Content-Type": "application/json",
      },
    }
  );
  const users = await response.json();
  console.log(users);
  usersListWrapperElem.innerHTML = "";
  users.results.forEach((user) => {
    usersListWrapperElem.insertAdjacentHTML(
      "beforeend",
      `
               <div class="flex items-center justify-between flex-wrap gap-4 py-2 px-4 border border-neutral-300 rounded-2xl">
                        <!-- Right: Checkbox | Image | Username | Email | Phone | Role -->
                        <div class="flex items-center gap-y-2 gap-x-4 flex-wrap">
                            <div class="flex items-center gap-x-4 w-full sm:w-auto md:w-full lg:w-auto">
                                <!-- Checkbox -->
                                <label class="relative inline-block">
                                    <input type="checkbox" class="peer absolute appearance-none w-full h-full bg-transparent cursor-pointer">
                                    <span class="size-6 flex justify-center items-center border-2 border-rose-500 peer-checked:bg-rose-500 rounded-md transition-colors"></span>
                                </label>
                                <!-- Image -->
                                <div class="size-[72px] rounded-xl overflow-hidden">
                                    <img class="size-full object-cover" src="${
                                      user.avatar_link
                                        ? user.avatar_link
                                        : "../images/avatar-2.jpg"
                                    }" alt="کفش">
                                </div>
                            </div>

                            <!-- Username -->
                            <span>${user.username}</span>

                            <!-- Email -->
                            <span>${
                              user.email ? user.email : "وارد نشده"
                            }</span>

                            <!-- Phone -->
                            <span>${
                              user.phone ? user.phone : "وارد نشده"
                            }</span>

                            <!-- Role -->
                            <span>${
                              user.role === "admin" ? "ادمین" : "کاربر"
                            }</span>

                        </div>

                        <!-- Buttons: Edit Btn | Delete Btn-->
                        ${
                          users.sender_root_access
                            ? `
                           <div class="flex items-center gap-2 justify-end grow">
                            <!-- Edit Btn -->
                            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#edit"></use>
                            </svg>

                            <!-- Delete Btn -->
                            <svg onclick="removeUser(${user.root_access} , '${user.username}')" class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                        `
                            : ""
                        }
                    </div>
    `
    );
  });
};

const removeUser = async (isRootAccess, username) => {
  if (!isRootAccess) {
    console.log(isRootAccess);
    askSwal(
      "آیا مطمئن به حذف کاربر مورد نظر خود هستید؟",
      undefined,
      "warning",
      "بله مطمئنم",
      "خیر",
      async (result) => {
        if (result.isConfirmed) {
          const response = await fetch(
            `http://localhost:8000/api/admin/user-management/list/delete_users_admins`,
            {
              method: "DELETE",
              headers: {
                Authorization: `Bearer ${getToken()}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                usernames: [username],
              }),
            }
          );
          console.log(response);
          if (response) {
            showSwal(
              "کاربر مورد نظر با موفقیت حذف شد.",
              "success",
              "متشکرم",
              () => {
                getAndShowAllUsers(true, true, 1, 6);
              }
            );
          } else {
            showSwal(
              "متاسفانه خطایی رخ داده است مجددا تلاش فرمایید.",
              "error",
              "متوجه شدم",
              () => {}
            );
          }
        }
      }
    );
  } else {
    showSwal(
      "شما مجاز به حذف ادمین مورد نظر نیستید.",
      "error",
      "متوجه شدم",
      () => {}
    );
  }
};

export { getAndShowAllUsers, removeUser };
