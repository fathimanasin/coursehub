// Form submission with AJAX
$(document).ready(function() {
    $('#enrollForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/enroll',
            data: $(this).serialize(),
            success: function(response) {
                window.location.href = '/'; // Redirect to homepage
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseText);
            }
        });
    });
});

