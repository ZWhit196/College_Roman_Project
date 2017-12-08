var chartColors = {
    white: 'rgb(255, 255, 255)', red: 'rgb(244, 110, 85)', lightRed: 'rgb(246, 131, 111)', blue: 'rgb(80,186,181)', lightBlue: 'rgb(162,210,212)', 
    green: 'rgb(6, 221, 135)', lightGreen: 'rgb(123, 237, 191)', lightGrey: 'rgb(229, 229, 229)', yellow: 'rgb(244,194,49)' 
};
var o, cb, er;

$(document).ready(function($) {
	o = {"start": true}
	cb = CallCharts;
	er = error_catch;
	var data = ajaxCall(o, cb, er);
	o = null, cb = null, er = null;
});

function ajaxCall(obj, callback, err) {
    $.ajax({
        url: window.location,
        method: 'POST',
        data: JSON.stringify( obj ),
        contentType: 'application/json'
    }).done(function(dt) { 
        if (dt.Response == 400 || dt.Error) {
            console.log("Failed processing");
            err();
        } else {
            callback(dt);
        }
    }).fail(function() {
        console.log("Failed processing");
        err();
    });
}

function CallCharts(data) {
	console.log("data", typeof data, data);
	data = JSON.parse(data)
	var tls = [], nls = [];
	var tvl = [], nvl = [];
	var ts = data.Times;
	var ns = data.Numbers;
	console.log(ts, ns);
	for (x=0;x<ts.length;x++) {
		tls.push( ts[x][0] );
		tvl.push( ts[x][1] );
	}
	for (x=0;x<ns.length;x++) {
		nls.push( ns[x][0] );
		nvl.push( ns[x][1] );
	}
	console.log(nls, nvl);
	console.log(tls, tvl);
	buildLineChart(tls, tvl, "stats1", "green");
	buildBarChart(nls, nvl, "stats2", "blue");
}


function buildLineChart(labels, data, elid, colour) {
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

function buildBarChart(labels, data, elid, colour) {
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

function error_catch() {
	alert("There was an issue retrieving your data. Please try again in a moment.");
}