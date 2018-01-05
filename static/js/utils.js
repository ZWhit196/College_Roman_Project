var chartColors = {
    white: 'rgb(255, 255, 255)', red: 'rgb(244, 110, 85)', lightRed: 'rgb(246, 131, 111)', blue: 'rgb(80,186,181)', lightBlue: 'rgb(162,210,212)', 
    green: 'rgb(6, 221, 135)', lightGreen: 'rgb(123, 237, 191)', lightGrey: 'rgb(229, 229, 229)', yellow: 'rgb(244,194,49)' 
};
var chartSelection = {}, gaugeSelection = {};
var ajaxobj = null, callback = null, errorback = null, showncol = null;


function SetAjaxArgs(o, c, e) { ajaxobj = o; callback = c; errorback = e; }

function NullAjaxArgs() { ajaxobj = null; callback = null; errorback = null; }

function AjaxCall() {
    $.ajax({
        url: window.location,
        method: 'POST',
        data: JSON.stringify( ajaxobj ),
        contentType: 'application/json'
    }).done(function(dt) {
        callback(dt);
        NullAjaxArgs();
    }).fail(function(e) {
        var m = JSON.parse(e.responseText).Message;
        errorback( m, e.status );
        NullAjaxArgs();
    });
}

function CallError(m,s) { console.log(s+": "+m); alert("There was an issue retrieving your data: "+m); }

function togglePassField(el) {
    // Toggle readability of password field given, switch between hidden text and readable text.
    if ( $( el ).prop("type") == "password" ) {
        $( el ).prop("type", "text");
        $( el ).prop("placeholder", "password");
    } else {
        $( el ).prop("type", "password");
        $( el ).prop("placeholder", "********");
    }
}

function isMatch(str1, str2) { if (str1 == str2) { return true; } return false; }

function isInArray(target, array) {
  for(var i = 0; i < array.length; i++) {
    if(array[i] === target) { return true; }
  }
  return false; 
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

function buildGauge(avg, id) {
    var op = setOp();
    var el = document.getElementById( id );
    var gauge = new Gauge( el ).setOptions( op );
    gauge.maxValue = 100;
    gauge.minValue = -100;
    gauge.animationSpeed = 32;
    gauge.set( avg );
    
    gaugeSelection[ id ] = gauge;
}
function setOp() {
    return {
        angle: 0.15, /* The span of the gauge arc */
        lineWidth: 0.44, /* The line thickness */
        radiusScale: 1, /* Relative radius*/
        pointer: {
            length: 0.6, /* Relative to gauge radius*/
            strokeWidth: 0.035, /* The thickness*/
            color: '#000000' /* Fill color*/
        },
        limitMax: true,     /* If false, the max value of the gauge will be updated if value surpass max*/
        limitMin: true,     /* If true, the min value of the gauge will be fixed unless you set it manually*/
        colorStart: '#6FADCF',   /* Colors*/
        colorStop: '#8FC0DA',    /* just experiment with them*/
        strokeColor: '#E0E0E0',  /* to see which ones work best for you*/
        generateGradient: true,
        percentColors: [[0.0, "#ff0000"], [0.5, "#FFFF2A"], [1.0, "#00FF00"]],
        staticLabels: {
            font: "16px sans-serif",  /* Specifies font*/
            labels: [-100, 0, 100],  /* Print labels at these values*/
            color: "#000000",  /* Optional: Label text color*/
            fractionDigits: 0  /* Optional: Numerical precision. 0=round off.*/
        },
        highDpiSupport: true    /* High resolution support*/
    };
}