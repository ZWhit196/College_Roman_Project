$(document).ready(function($) {
    $("#submit").click(function(){
        var v = $("#value").val();
        SetAjaxArgs( {"val": v}, ShowVal, CallError );
        AjaxCall();
    });
});


function ShowVal(dt) {
    $("#result").find("p").remove();
    if (dt.base != "Roman") $("#result").append("<p>The Roman numeral for this value is "+dt.val+"</p>");
    else $("#result").append("<p>The value for this Roman numeral is "+dt.val+"</p>");
}