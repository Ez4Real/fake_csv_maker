window.setTimeout(function() {
  $(".alert").fadeTo(500, 0).slideUp(500, function(){
      $(this).remove();
  });
}, 3000);

// Handle dropdown menu
$('.dropdown-toggle').hover(function() {
$(this).parent().find('.dropdown-menu').first().stop(true, true).delay(100).slideDown(250);
}, function() {
$(this).parent().find('.dropdown-menu').first().stop(true, true).delay(100).slideUp(250);
});