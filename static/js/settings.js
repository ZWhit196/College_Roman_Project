$(document).ready(function($) {
    $("#theme-select").val(theme);
    
    $("#theme-select").change(function() {
        $("#theme").val( $(this).find("option:selected").val() );
    });
});