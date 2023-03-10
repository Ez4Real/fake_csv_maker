const toggleField = (column) => {
  const { value: fieldType } = column.querySelector('.type-field');
  const fromParent = column.querySelector('.from-field-td');
  const toParent = column.querySelector('.to-field-td');
  const [fromLabel, fromInput] = Array.from(fromParent.children);
  const [toLabel, toInput] = Array.from(toParent.children);
  const display = fieldType === 'Integer' ? 'block' : 'none';
  [fromLabel, fromInput, toLabel, toInput].forEach(el => el.style.display = display);
}

const addRangesToggle = (column) => {
  toggleField(column);
  column.querySelector('.type-field').addEventListener('change', () => {
    toggleField(column);
  });
}

const initialFormsToggle = document.querySelectorAll('.formset-row');
initialFormsToggle.forEach((form) => {
  addRangesToggle(form);
})

