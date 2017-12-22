var ajaxobj = null, callback = null, errorback = null;

$(document).ready(function($){
    $("#flash-msg").find("span").click(function(){ CloseMessages(); });
    $(".logo").click(function(){ window.location = "/"; });
});

function CloseMessages() { $("#flash-msg").remove(); }

function SetAjaxArgs(o, c, e) { ajaxobj = o; callback = c; errorback = e; }

function NullAjaxArgs() { ajaxobj = null; callback = null; errorback = null; }

function AjaxCall() {
    $.ajax({
        url: window.location,
        method: 'POST',
        data: JSON.stringify( ajaxobj ),
        contentType: 'application/json'
    }).done(function(dt) {
        NullAjaxArgs();
        if (dt.Response == 400 || dt.Error) {
            console.log("Failed processing");
            errorback();
        } else {
            callback(dt);
        }
    }).fail(function() {
        NullAjaxArgs();
        console.log("Failed processing");
        errorback();
    });
}

function BuildLineChart(labels, data, elid, colour) {
    var YAobj = { ticks: { beginAtZero: true }, display: true,scaleLabel: {display: true}};
    var config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                lineTension: 0,
                borderWidth: 1,
                backgroundColor: chartColors[colour],
                borderColor: chartColors[colour],
                data: data,
                fill: false,
            }]
        },
        options: { 
            legend: { display: false },
            responsive: true,
            title:{display:false,text:'Data'}, hover: {mode: 'nearest',intersect: true},
            scales: {xAxes: [{display: true,scaleLabel: {display: true,}}],
                    yAxes: [YAobj]},
        }
    };
    var chart = new Chart(document.getElementById( elid ).getContext("2d"), config);
}

function BuildBarChart(labels, data, elid, colour) {
    var YAobj = { ticks: { beginAtZero: true }, display: true,scaleLabel: {display: true}};
    var config = {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                borderWidth: 1,
                backgroundColor: chartColors[colour],
                borderColor: chartColors[colour],
                data: data,
                fill: false,
            }]
        },
        options: { 
            legend: { display: false },
            responsive: true,
            title:{display:false,text:'Data'}, hover: {mode: 'nearest',intersect: true},
            scales: {xAxes: [{display: true,scaleLabel: {display: true,}}],
                    yAxes: [YAobj]},
        }
    };
    var chart = new Chart(document.getElementById( elid ).getContext("2d"), config);
}

function CallError() { alert("There was an issue retrieving your data. Please try again in a moment."); }