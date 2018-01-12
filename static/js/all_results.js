
$(document).ready(function($) {
    SetAjaxArgs( {"get": 0}, CreateInterface, CallError );
    AjaxCall();
});

function CreateInterface(data) {
    var table, prev, next, pagenum=getParameterByName("page");

    if (!pagenum) pagenum = 1;
    if (data.length == 10) next="<div id='pager'> </div>";
    if (pagenum !== 1) prev="";

    table = BuildTable(data);
    $("#all").append( table );
}

function BuildTable(dt) {
    var i, table = "<table> <thead> <th>Value</th> <th>Base</th> <th>Roman</th> <th>Date Converted</th> </thead> <tbody>";
    for (i=0; i<dt.length; i++) table += "<td>"+dt[i].Value+"</td> <td>"+dt[i].Base_value+"</td> <td>"+dt[i].Roman+"</td> <td>"+dt[i].Date+"</td>";
    table += "</tbody> </table>";
    return table;
}

