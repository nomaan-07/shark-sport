import { getToken, showSwal } from "../../../../scripts/funcs/utils.js";

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
                                      user.avatar_link ? user.avatar_link : "../images/avatar-2.jpg"
                                    }" alt="کفش">
                                </div>
                            </div>

                            <!-- Username -->
                            <span>${user.username}</span>

                            <!-- Email -->
                            <span>${user.email ? user.email : "وارد نشده"}</span>

                            <!-- Phone -->
                            <span>${user.phone ? user.phone : "وارد نشده"}</span>

                            <!-- Role -->
                            <span>${
                              user.role === "admin" ? "ادمین" : "کاربر"
                            }</span>

                        </div>

                        <!-- Buttons: Edit Btn | Delete Btn-->
                        <div class="flex items-center gap-2 justify-end grow">
                            <!-- Edit Btn -->
                            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#edit"></use>
                            </svg>

                            <!-- Delete Btn -->
                            <svg class="size-6 sm:cursor-pointer text-rose-500 sm:hover:text-rose-700 transition-colors">
                                <use href="#trash"></use>
                            </svg>
                        </div>
                    </div>
    `
    );
  });
};

export { getAndShowAllUsers };
