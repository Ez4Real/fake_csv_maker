$(document).ready(function() {
    $("#generate-data-form").on("submit", function(event) {
      event.preventDefault();
      var form = $(this);
      $.post(form.attr("action"), form.serialize(), function(response) {
        generateDataset(response.dataset_id);
      }).fail(function(xhr, status, error) {
      });
    });
  });
  
  function generateDataset(datasetId) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.post("/generate-dataset/", {
      csrfmiddlewaretoken: csrf_token,
      dataset_id: datasetId
    }, function(response) {
      console.log(response);
    }).fail(function(xhr, status, error) {
      console.log(error);
    });
  }