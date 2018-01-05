var chartColors = {
    white: 'rgb(255, 255, 255)', red: 'rgb(244, 110, 85)', lightRed: 'rgb(246, 131, 111)', blue: 'rgb(80,186,181)', lightBlue: 'rgb(162,210,212)', 
    green: 'rgb(6, 221, 135)', lightGreen: 'rgb(123, 237, 191)', lightGrey: 'rgb(229, 229, 229)', yellow: 'rgb(244,194,49)' 
};


$(document).ready(function($) {
	SetAjaxArgs( {"get": "stats"}, CallCharts, CallError );
	AjaxCall();
});


function CallCharts(data) {
	console.log("data", typeof data, data);
	var time_keys = data.weekUse.dates, time_vals = data.weekUse.volumes; // time datasets
	var vol_keys = data.top5.values, vol_vals = data.top5.counts; // volume datasets
	if (time_keys && time_vals) BuildLineChart(time_keys, time_vals, "use-on-time", "green");
	if (vol_keys && vol_vals) BuildBarChart(vol_keys, vol_vals, "popular-conversion", "blue");
}
