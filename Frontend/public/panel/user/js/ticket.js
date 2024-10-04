import { toggleSelect, selectOption } from '../../js/ui/ui-handlers.js';

const levelSelect = document.querySelector('.panel-select');
const levelSelectHeaderEl = document.querySelector('.panel-select__header');
const selectedLevelEl = document.querySelector(
    '.panel-select__selected-option'
);
const levelIcon = document.querySelector('.panel-select__icon');
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
            'panel-select--active',
            'panel__option--active'
        );

        toggleSelect(levelIcon, levelOptionsWrapperEl, 'panel-select--active');
    });
});

levelSelectHeaderEl.addEventListener('click', () =>
    toggleSelect(levelIcon, levelOptionsWrapperEl, 'panel-select--active')
);
