import { toggleSelect, selectOption } from '../../../js/ui/ui-handlers.js';

const filterEl = document.querySelector('.panel-filter');
const filterHeaderEl = document.querySelector('.panel-filter__header');
const selectedFilterEl = document.querySelector('.panel-filter__selected');
const filterIcon = document.querySelector('.panel-filter__icon');
const filterOptionsWrapper = document.querySelector(
    '.panel-filter__options-wrapper'
);
const filterOptions = document.querySelectorAll('.panel-filter__option');

const sortEl = document.querySelector('.panel-sort');
const sortHeaderEl = document.querySelector('.panel-sort__header');
const selectedSortEl = document.querySelector('.panel-sort__selected');
const sortIcon = document.querySelector('.panel-sort__icon');
const sortOptionsWrapper = document.querySelector(
    '.panel-sort__options-wrapper'
);
const sortOptions = document.querySelectorAll('.panel-sort__option');

filterOptions.forEach((option) => {
    option.addEventListener('click', () => {
        selectOption(
            filterEl,
            selectedFilterEl,
            filterOptions,
            option,
            'filter',
            'panel-filter__active',
            'panel-filter__option--active'
        );

        toggleSelect(filterIcon, filterOptionsWrapper, 'panel-filter__active');
    });
});

filterHeaderEl.addEventListener('click', () =>
    toggleSelect(filterIcon, filterOptionsWrapper, 'panel-filter__active')
);

sortOptions.forEach((option) => {
    option.addEventListener('click', () => {
        selectOption(
            sortEl,
            selectedSortEl,
            sortOptions,
            option,
            'sort',
            'panel-sort__active',
            'panel-sort__option--active'
        );

        toggleSelect(sortIcon, sortOptionsWrapper, 'panel-sort__active');
    });
});

sortHeaderEl.addEventListener('click', () =>
    toggleSelect(sortIcon, sortOptionsWrapper, 'panel-sort__active')
);
