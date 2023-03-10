$(document).ready(function() {
    $('#generate-data-form').submit(function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        
        // Send an AJAX request to the server
        $.ajax({
            url: '/generate-data/',
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                // Handle the response from the server
                if (response.status === 'success') {
                    alert(response.message);
                } else {
                    alert('Error generating data');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });
});