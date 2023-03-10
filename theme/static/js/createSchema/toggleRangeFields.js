const toggleField = (column) => {
  const show = column.querySelector('.type-field').value === 'Integer' ? 'block' : 'none';
  column.querySelector('.from-field-div').style.display = show;
  column.querySelector('.to-field-div').style.display = show;
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
  columns.forEach(addColumnToggle);
});

