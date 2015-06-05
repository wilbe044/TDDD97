/**
 * Created by wille on 15-06-05.
 */
// Get context with jQuery - using jQuery's .get() method
var pieChart;
var renderChart = function(online, offline) {
ctxFirst = document.getElementById("online-users-chart").getContext("2d")

        var data = [
    {
        value: online,
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Online"
    },
    {
        value: offline,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Offline"
    }
];

pieChart = new Chart(ctxFirst).Pie(data);

};


updateChart = function(total, diff) {
    pieChart.segments[0].value = total;
    pieChart.segments[1].value = diff;
    pieChart.update()
};