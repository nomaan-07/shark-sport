import { createTag } from "./funcs/add-tag.js";

window.addEventListener("load", () => {
  const addTagBtn = document.getElementById("add-tag-btn");
  addTagBtn.addEventListener("click", (e) => {
    e.preventDefault();
    createTag();
  });
});
