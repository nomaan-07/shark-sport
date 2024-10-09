const toggleSelect = (icon, optionsWrapper, selectActiveClass) => {
  icon.classList.toggle("rotate-180");
  icon.classList.toggle(selectActiveClass);
  optionsWrapper.classList.toggle("select-option--visible");
};

const selectOption = (
  select,
  selected,
  options,
  option,
  type,
  selectActiveClass,
  optionActiveClass
) => {
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
};

export { selectOption, toggleSelect };
