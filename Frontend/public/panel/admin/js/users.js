import { getAndShowAllUsers } from "./funcs/users.js";

window.addEventListener("load", () => {
    getAndShowAllUsers(true , 5 , 5);
})