var chartColors = {
    white: 'rgb(255, 255, 255)', red: 'rgb(244, 110, 85)', lightRed: 'rgb(246, 131, 111)', blue: 'rgb(80,186,181)', lightBlue: 'rgb(162,210,212)', 
    green: 'rgb(6, 221, 135)', lightGreen: 'rgb(123, 237, 191)', lightGrey: 'rgb(229, 229, 229)', yellow: 'rgb(244,194,49)' 
};


$(document).ready(function($) {
	SetAjaxArgs( {"get": "stats"}, CallCharts, CallError );
	AjaxCall();
});


function CallCharts(data) {
// 	console.log("data", typeof data, data);
	data = JSON.parse(data);
	var tls = [], nls = [];
	var tvl = [], nvl = [];
	var ts = data.Times;
	var ns = data.Numbers;
// 	console.log(ts, ns);
	for (x=0;x<ts.length;x++) {
		tls.push( ts[x][0] );
		tvl.push( ts[x][1] );
	}
	for (x=0;x<ns.length;x++) {
		nls.push( ns[x][0] );
		nvl.push( ns[x][1] );
	}
// 	console.log(nls, nvl);
// 	console.log(tls, tvl);
	buildLineChart(tls, tvl, "use-on-time", "green");
	buildBarChart(nls, nvl, "popular-conversion", "blue");
}


