import { toggleSelect, selectOption } from '../../../js/ui/ui-handlers.js';

const imageUploadButtons = document.querySelectorAll('.image-upload-btn');

const selectElementHeaders = document.querySelectorAll('.panel-select__header');

function handleSelect(el) {
    const type = el.dataset.type;
    const selectEl = document.querySelector(`.panel-select--${type}`);
    const selectedEl = document.querySelector(
        `.panel-select__selected-option--${type}`
    );
    const icon = document.querySelector(`.panel-select__icon--${type}`);
    const optionsWrapperEl = document.querySelector(
        `.panel__options-wrapper--${type}`
    );
    const optionElements = document.querySelectorAll(`.panel__option--${type}`);

    optionElements.forEach((option) => {
        option.addEventListener('click', () => {
            selectOption(
                selectEl,
                selectedEl,
                optionElements,
                option,
                type,
                'panel-select--active',
                'panel__option--active'
            );

            toggleSelect(icon, optionsWrapperEl, 'panel-select--active');
        });
    });

    el.addEventListener('click', () =>
        toggleSelect(icon, optionsWrapperEl, 'panel-select--active')
    );
}

selectElementHeaders.forEach((el) => handleSelect(el));

imageUploadButtons.forEach((btn) =>
    btn.addEventListener('click', () => btn.nextElementSibling.click())
);
