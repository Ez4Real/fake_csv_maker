const toggleField = (column) => {
  const { value: fieldType } = column.querySelector('.type-field');
  const fromParent = column.querySelector('.from-field-div');
  const toParent = column.querySelector('.to-field-div');
  const [fromLabel, fromInput] = Array.from(fromParent.children);
  const [toLabel, toInput] = Array.from(toParent.children);
  const display = fieldType === 'Integer' ? 'block' : 'none';
  [fromLabel, fromInput, toLabel, toInput].forEach(el => el.style.display = display);
}

const addColumnToggle = (column) => {
  toggleField(column);
  column.querySelector('.type-field').addEventListener('change', () => {
    toggleField(column);
  });
}

const initialColumn = document.querySelector('.initial-form');
addColumnToggle(initialColumn);

addButton.addEventListener('click', () => {
  const columns = document.querySelectorAll('.column-form');
  console.log(columns);
  columns.forEach(addColumnToggle);
});

