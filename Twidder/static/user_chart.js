/**
 * Created by wille on 15-06-05.
 */
// Get context with jQuery - using jQuery's .get() method
var doughnutChart;
var renderChart = function(online, offline) {
ctxFirst = document.getElementById("online-users-chart").getContext("2d")

        var data = [
    {
        value: online,
        color:"#6DE15E",
        highlight: "#AAFC9F",
        label: "Online"
    },
    {
        value: offline,
        color: "#DE5050",
        highlight: "#FDAAAA",
        label: "Offline"
    }
];

doughnutChart = new Chart(ctxFirst).Doughnut(data);

};


updateChart = function(online, offline) {
    doughnutChart.segments[0].value = online;
    doughnutChart.segments[1].value = offline;
    doughnutChart.update();
};