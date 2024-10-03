import { toggleSelect, selectOption } from '../../js/ui/ui-handlers.js';

const levelSelect = document.querySelector('.panel__select');
const levelSelectHeaderEl = document.querySelector('.panel__select-header');
const selectedLevelEl = document.querySelector('.selected-level');
const levelIcon = document.querySelector('.level__icon');
const levelOptionsWrapperEl = document.querySelector('.panel__options-wrapper');
const levelOptions = document.querySelectorAll('.panel__option');

levelOptions.forEach((option) => {
    option.addEventListener('click', () => {
        selectOption(
            levelSelect,
            selectedLevelEl,
            levelOptions,
            option,
            'level',
            'panel__select--active',
            'panel__option--active'
        );

        toggleSelect(levelIcon, levelOptionsWrapperEl, 'panel__select--active');
    });
});

levelSelectHeaderEl.addEventListener('click', () =>
    toggleSelect(levelIcon, levelOptionsWrapperEl, 'panel__select--active')
);
