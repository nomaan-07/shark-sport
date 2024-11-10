function toggleSelect(icon, optionsWrapper, selectActiveClass) {
  icon.classList.toggle("rotate-180");
  icon.classList.toggle(selectActiveClass);
  optionsWrapper.classList.toggle("hide");
}

function selectOption(
  select,
  selected,
  options,
  option,
  type,
  selectActiveClass,
  optionActiveClass
) {
  const optionDataset = option.dataset[type];
  select.dataset[type] = optionDataset;
  selected.textContent = option.textContent;

  options.forEach((el) => el.classList.remove(optionActiveClass));

  if (optionDataset === "null") {
    selected.classList.remove(selectActiveClass);
    return;
  }

  selected.classList.add(selectActiveClass);
  option.classList.add(optionActiveClass);
}

// Select Options Handler From Getting in APIs
const handleSelectOptions = (type) => {
  const optionElements = document.querySelectorAll(`.panel__option--${type}`);
  optionElements.forEach((option) => {
    option.addEventListener("click", () => {
      const selectEl = document.querySelector(`.panel-select--${type}`);
      const selectedEl = document.querySelector(
        `.panel-select__selected-option--${type}`
      );
      const icon = document.querySelector(`.panel-select__icon--${type}`);
      const optionsWrapperEl = document.querySelector(
        `.panel__options-wrapper--${type}`
      );
      selectOption(
        selectEl,
        selectedEl,
        optionElements,
        option,
        type,
        "panel-select--active",
        "panel__option--active"
      );
      toggleSelect(icon, optionsWrapperEl, "panel-select--active");
    });
  });
};

export { toggleSelect, selectOption, handleSelectOptions };
