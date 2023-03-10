const toggleRangeFields = () => {
    const rows = document.querySelectorAll('#column-formset-body tr')
    rows.forEach(row => {
      const type = row.querySelector('#id_form-0-type')
      const from = row.querySelector('.from')
      const to = row.querySelector('.to')
      const fromHeader = document.querySelector('.from-header')
      const toHeader = document.querySelector('.to-header')
  
      const toggleFields = () => {
        const show = type.value === 'Integer' ? 'table-cell' : 'none'
        from.style.display = show
        to.style.display = show
        fromHeader.style.display = show
        toHeader.style.display = show
      }
      toggleFields()
      type.addEventListener('change', toggleFields)
    })
  }
  
toggleRangeFields()

// $(document).ready(function() {
//     var addButton = $('#add-column-btn');
//     var deleteButton = $('#delete-row-btn');
//     var formCount = $('#id_form-TOTAL_FORMS').val();
//     var formTable = $('#column-formset-body');

//     // add column form field dynamically
//     addButton.click(function() {
//         var newForm = $('.formset-empty').clone().removeClass('formset-empty').addClass('row-' + formCount);
//         newForm.find(':input').each(function() {
//             var name = $(this).attr('name').replace('-empty', '-' + formCount);
//             var id = 'id_' + name;
//             $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
//         });
//         newForm.find('.from').hide();
//         newForm.find('.to').hide();
//         newForm.find('.from-header').hide();
//         newForm.find('.to-header').hide();
//         newForm.append(deleteButton);
//         formTable.append(newForm);
//         formCount++;
//         $('#id_form-TOTAL_FORMS').val(formCount);
//     });

//     // delete column form field dynamically
//     $(document).on('click', '.delete-row', function() {
//         var currentForm = $(this).closest('tr');
//         currentForm.find(':input').each(function() {
//             var name = $(this).attr('name');
//             if (name.indexOf('-empty') === -1) {
//                 var newId = 'id_' + name.replace(/\d+/g, function(match) {
//                     return parseInt(match) - 1;
//                 });
//                 $(this).attr({'name': name.replace(/\d+/g, function(match) {
//                     return parseInt(match) - 1;
//                 }), 'id': newId}).val('');
//             }
//         });
//         currentForm.remove();
//         formCount--;
//         $('#id_form-TOTAL_FORMS').val(formCount);
//     });

//     // display range_start and range_end fields when type is Integer
//     $(document).on('change', '#id_form-0-type', function() {
//         var currentForm = $(this).closest('tr');
//         var rangeStart = currentForm.find('.from');
//         var rangeEnd = currentForm.find('.to');
//         var fromHeader = currentForm.find('.from-header');
//         var toHeader = currentForm.find('.to-header');

//         if ($(this).val() === 'Integer') {
//             rangeStart.show();
//             rangeEnd.show();
//             fromHeader.show();
//             toHeader.show();
//         } else {
//             rangeStart.hide();
//             rangeEnd.hide();
//             fromHeader.hide();
//             toHeader.hide();
//         }
//     });
// });
