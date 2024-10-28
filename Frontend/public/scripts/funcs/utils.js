const showSwal = (text, icon, confirmButtonText, callback) => {
  Swal.fire({
    text,
    icon,
    confirmButtonText,
  }).then((result) => callback(result));
};

const showToast = (position, timer, icon, title) => {
  Swal.mixin({
    position,
    timer,
    toast: true,
    showConfirmButton: false,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    },
  }).fire({
    icon,
    title,
  });
};

const saveIntoLocalStorage = (key, value) => {
  return localStorage.setItem(key, JSON.stringify(value));
};

const getFromLocalStorage = (key) => {
  return JSON.parse(localStorage.getItem(key));
};

const getToken = () => {
  const userInfos = JSON.parse(localStorage.getItem("user"));
  return userInfos ? userInfos.token : null;
};

const isLogin = () => {
  const userInfos = localStorage.getItem("user");
  return userInfos ? true : false;
};

const getUrlParam = (key) => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(key) || null;
};

const searchInArray = (array, searchProperty, searchValue) => {
  let outputArray = array.filter((item) =>
    item[searchProperty].includes(searchValue)
  );
  return outputArray;
};

const convertDate = (date) => {
  let datePersian = new Date(date).toLocaleDateString("fa-Ir");
  return datePersian;
};

const formatNumber = (value) => {
  return new Intl.NumberFormat("fa-IR").format(value);
};

export {
  showSwal,
  showToast,
  saveIntoLocalStorage,
  getFromLocalStorage,
  getToken,
  isLogin,
  getUrlParam,
  searchInArray,
  convertDate,
  formatNumber,
};
