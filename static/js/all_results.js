
$(document).ready(function($) {
    SetAjaxArgs( {"get": 0}, CallTable, CallError );
    AjaxCall();
});

function CallTable(dt) {
    console.log(typeof dt, dt);
}