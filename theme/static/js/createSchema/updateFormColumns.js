$(function() {
  const formset = $('#formset tbody')
  const lastForm = $('#formset tbody .last-form');
  const formTemplate = lastForm.clone(true)
  lastForm.find('.delete-column-btn').remove();
  const maxForms = parseInt($('#id_columns-MAX_NUM_FORMS').val())
  let totalForms = parseInt($('#id_columns-TOTAL_FORMS').val())

  const addForm = () => {
    const formsetCount = formset.children('.formset-row').length
    if (formsetCount >= maxForms) return

    const newForm = formTemplate.clone(true).removeClass('last-form')

    newForm.find('input, select').each(function(index, input) {
      const inputName = $(input).attr('name').replace(/-\d+/, '-' + formsetCount)
      const lastInput = lastForm.find('[name="'+$(input).attr('name')+'"]')
      $(input).attr({'name': inputName, 'id': 'id_' + inputName}).val(lastInput.val())
    })

    lastForm.find('input, select').each(function(index, input) {
      input.nodeName === 'SELECT' ? input.selectedIndex = 0 : input.value = ''
    })
    addRangesToggle(lastForm[0])

    $('#formset .formset-row:not(".formset-initial"):last').before(newForm)
    
    addRangesToggle(newForm[0])

  }

  $('.add-column-btn').on('click', addForm);

  formset.on('click', '.delete-column-btn', function() {
    $(this).closest('.formset-row').remove()
    $('#id_columns-TOTAL_FORMS').val(--totalForms)
  })
})