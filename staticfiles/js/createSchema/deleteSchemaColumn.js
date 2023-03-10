$(document).on("click", ".delete-row-btn", function() {
    $(this).closest("tr").find("input[name$='-DELETE']").prop("checked", true);
    $(this).closest("tr").hide();
});