$(document).ready(function() {
  $("#generate-data-form").on("submit", function(event) {
      event.preventDefault()
      var form = $(this)
      $.post(form.attr("action"), form.serialize(), function(response) {
        console.log();
        generateDataset(response.dataset_id)
      }).fail(function(xhr, status, error) {
        var response = JSON.parse(xhr.responseText)
        displayErrors(response.errors)
      })
  })
})

function displayErrors(errors) {
  var alert_div = $("<div>").addClass("flex justify-center");
  $.each(errors, function(field, field_errors) {
    $.each(field_errors, function(i, error) {
      var error_msg = $("<div>")
        .addClass("alert text-center p-4 rounded-lg border border-dark shadow-md bg-red text-white")
        .text(field + ": " + error);
      alert_div.append(error_msg);
    });
  });
  $("main").prepend(alert_div);
  setTimeout(function() {
    alert_div.remove();
  }, 3000);
}

function generateDataset(datasetId) {
  var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
  $.ajax({
      type: "POST",
      url: "/generate-dataset/",
      data: {
          csrfmiddlewaretoken: csrf_token,
          dataset_id: datasetId
      },
      async: true,
      success: function(response) {
          setTimeout(function() {
              console.log(response)
              location.reload()
          }, 2000)
      },
      error: function(xhr, status, error) {
        var response_data = JSON.parse(xhr.responseText)
        displayErrors(response_data.errors)
      }
  })
}