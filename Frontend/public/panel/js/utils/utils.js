const setToLocalStorage = (key, value) => localStorage.setItem(key, value)

const getFromLocalStorage = (key) => localStorage.getItem(key)

export {setToLocalStorage, getFromLocalStorage}