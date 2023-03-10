$(document).on("click", "#add-column-btn", function() {
    var row = $("#column-formset-body tr:first").clone();
    var totalForms = $("#id_form-TOTAL_FORMS").val();
    var newRowOrder = parseInt(row.find("input[name$='order']").val()) + 1;
    row.find("input").each(function() {
        var name = $(this).attr("name").replace(/-\d+-/, "-" + totalForms + "-");
        var id = "id_" + name;
        $(this).attr({"name": name, "id": id}).val("");
    });
    row.find(".delete-row-btn").show();
    row.find("input[name$='order']").val(newRowOrder);
    $("#id_form-TOTAL_FORMS").val(parseInt(totalForms) + 1);
    $("#column-formset-body").append(row);
});