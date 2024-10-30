const setToLocalStorage = (key, value) => localStorage.setItem(key, value);

const getFromLocalStorage = (key) => localStorage.getItem(key);

const logout = () => {
  localStorage.removeItem("user");
  return true;
};

export { setToLocalStorage, getFromLocalStorage, logout };
