import { setToLocalStorage, getFromLocalStorage } from '../utils/utils.js';

const changeThemeBtn = document.querySelector('.theme-btn');
const moonIcon = document.querySelector('#moon-icon');
const sunIcon = document.querySelector('#sun-icon');

const sidebarOpenBtn = document.querySelector('#sidebar-open-btn');
const sidebarCloseBtn = document.querySelector('#sidebar-close-btn');

const panelSidebar = document.querySelector('.panel__sidebar');

const overlay = document.querySelector('#overlay');

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

function sidebarToggleHandler() {
    panelSidebar.classList.toggle('-translate-x-80');
    overlay.classList.toggle('hidden');
    document.body.classList.toggle("overflow-hidden");
}

changeThemeBtn.addEventListener('click', themeBtnClickHandler);
sidebarOpenBtn.addEventListener('click', sidebarToggleHandler);
sidebarCloseBtn.addEventListener('click', sidebarToggleHandler);
overlay.addEventListener('click', sidebarToggleHandler);

window.addEventListener('resize', (e) => {
    if (e.target.innerWidth < 992) return;

    panelSidebar.classList.remove('-translate-x-80');
    overlay.classList.add('hidden');
});

window.addEventListener('load', localThemeHandler);
