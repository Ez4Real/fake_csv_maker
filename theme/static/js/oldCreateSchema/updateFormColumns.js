const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
const formsetContainer = totalFormsInput.parentNode;
const addButton = formsetContainer.querySelector('.add-column-btn');
const initialForm = formsetContainer.querySelector('.initial-form');
const formTemplate = initialForm.cloneNode(true);

initialForm.querySelector('button[id="delete-column-btn"]').remove()

function updateForm(form, index) {
  const inputs = form.querySelectorAll('input, select');
  inputs.forEach((input) => {
    ['name', 'id'].forEach((attr) => {
      input.setAttribute(attr, input.getAttribute(attr).replace(/-\d+-/, `-${index}-`));
    });
  });
  const deleteBtn = form.querySelector('#delete-column-btn');
  console.log(deleteBtn);
  deleteBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (confirm('Are you sure you want to delete this column?')) {
      deleteForm(form);
    }
  });
}

function deleteForm(form) {
  form.remove();
  totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
}

function resetForm(form) {
  const inputs = form.querySelectorAll('input, select');
  inputs.forEach((input) => {
    if (input.nodeName === 'SELECT') {
      input.selectedIndex = 0;
    } else {
      input.value = input.defaultValue;
    }
  });
}

addButton.addEventListener('click', (e) => {
  e.preventDefault();
  const totalFormsNum = parseInt(totalFormsInput.value);
  const newForm = formTemplate.cloneNode(true);
  newForm.classList.remove('initial-form');
  updateForm(newForm, totalFormsNum);
  totalFormsInput.value = totalFormsNum + 1;
  formsetContainer.insertBefore(newForm, addButton.parentNode);
  const newFormInputs = newForm.querySelectorAll('input, select');
  const starterFormInputs = initialForm.querySelectorAll('input, select');
  newFormInputs.forEach((input, index) => {
    input.value = starterFormInputs[index].value;
  });
  resetForm(initialForm);
});