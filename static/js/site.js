var ajaxobj = null, callback = null, errorback = null;

$(document).ready(function($){
    $("#flash-msg").find("span").click(function(){ CloseMessages(); });
    $(".logo").click(function(){ window.location = "/"; });
});

function CloseMessages() { $("#flash-msg").remove(); }