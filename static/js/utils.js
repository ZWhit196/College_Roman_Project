var chartColors = {
    white: 'rgb(255, 255, 255)', red: 'rgb(244, 110, 85)', lightRed: 'rgb(246, 131, 111)', blue: 'rgb(80,186,181)', lightBlue: 'rgb(162,210,212)', 
    green: 'rgb(6, 221, 135)', lightGreen: 'rgb(123, 237, 191)', lightGrey: 'rgb(229, 229, 229)', yellow: 'rgb(244,194,49)' 
};
var chartSelection = {}, gaugeSelection = {};

var ajaxobj = null, callback = null, errorback = null, showncol = null;


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

function SetAjaxArgs(o, c, e) { ajaxobj = o; callback = c; errorback = e; }

function NullAjaxArgs() { ajaxobj = null; callback = null; errorback = null; }

function ajaxCall(obj, callback, err) {
    $.ajax({
        url: window.location,
        method: 'POST',
        data: JSON.stringify( obj ),
        contentType: 'application/json'
    }).done(function(dt) {
        NullAjaxArgs();
        if (dt.Response == 400 || dt.Error) { // UPDATED - REMOVE IF STATEMENT
            console.log("Failed processing");
            err();
        } else { callback(dt); }
    }).fail(function() {
        NullAjaxArgs();
        console.log("Failed processing");
        err();
    });
}

function isMatch(str1, str2) { if (str1 == str2) { return true; } return false; }

function sentimentEval( snt ) {
//     return (Math.round(( snt*100) +"e+2")+"e-2"); // OLD METHOD
    if (snt === null) { return snt; } return (Math.round( snt*100 ));
}

function isInArray(target, array) {
  for(var i = 0; i < array.length; i++) {
    if(array[i] === target) { return true; }
  }
  return false; 
}

// http://stackoverflow.com/questions/4565112/javascript-how-to-find-out-if-the-user-browser-is-chrome/13348618#13348618
function isChrome() {
    var isChromium = window.chrome,
        winNav = window.navigator,
        vendorName = winNav.vendor,
        isOpera = winNav.userAgent.indexOf("OPR") > -1,
        isIEedge = winNav.userAgent.indexOf("Edge") > -1,
        isIOSChrome = winNav.userAgent.match("CriOS");
    if(isIOSChrome){ return true;
    } else if(isChromium !== null && isChromium !== undefined && vendorName === "Google Inc." && isOpera == false && isIEedge == false) { return true;
    } else { return false; }
}

// CURRENTLY UNUSED
function buildLineChart(labels, data, elid, colour, restrAx) {
    var YAobj;
    if (restrAx) { YAobj = { ticks: { beginAtZero: false, fixedStepSize: 25, suggestedMax: 100, suggestedMin: -100 }, display: true,scaleLabel: {display: true}};
    } else { YAobj = { display: true,scaleLabel: {display: true}}; }
    
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
            responsive: true,
            title:{display:false,text:'Data'}, hover: {mode: 'nearest',intersect: true},
            scales: {xAxes: [{display: true,scaleLabel: {display: true,}}],
                    yAxes: [YAobj]},
        }
    };
    var chart = new Chart(document.getElementById( elid ).getContext("2d"), config);
    chartSelection[ elid ] = chart;
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