import { setToLocalStorage, getFromLocalStorage } from '../utils/utils.js';

const changeThemeBtn = document.querySelector('.theme-btn');
const moonIcon = document.querySelector('#moon-icon');
const sunIcon = document.querySelector('#sun-icon');

function changeThemeHandler(theme) {
    document.documentElement.className = theme;

    if (theme === 'dark') {
        moonIcon.classList.add('hidden');
        sunIcon.classList.remove('hidden');
        changeThemeBtn.dataset.theme = 'light';
    } else {
        moonIcon.classList.remove('hidden');
        sunIcon.classList.add('hidden');
        changeThemeBtn.dataset.theme = 'dark';
    }
}
function themeBtnClickHandler() {
    const theme = changeThemeBtn.dataset.theme;

    setToLocalStorage('theme', theme);

    changeThemeHandler(theme);
}

function localThemeHandler() {
    const localTheme = getFromLocalStorage('theme');

    if (!localTheme) return;

    changeThemeHandler(localTheme);
}

changeThemeBtn.addEventListener('click', themeBtnClickHandler);

window.addEventListener('load', () => {
    localThemeHandler();
});
