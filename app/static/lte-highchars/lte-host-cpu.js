var chart;
var chart1;
/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
        $.ajax({
        url: '/info/data/host-cpu',
        success: function(point) {
            var x = document.getElementById("setinterval-cpu").value;
            var y = parseInt(x);
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);
            chart.redraw();
            // call it again after one second
            setTimeout(requestData, y);
        },
        cache: true
    });
}

function requestData1() {
    $.ajax({
        url: '/info/data/host-mem',
        success: function(point) {
            var x1 = document.getElementById("setinterval-mem").value;
            var y1 = parseInt(x1);
            var series = chart1.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart1.series[0].addPoint(point, true, shift);
            chart1.redraw();
            // call it again after one second
            setTimeout(requestData1, y1);
        },
        cache: true
    });
}

/*function requestData() {
    $.ajax({
        url: '/info/data/host-cpu',
        success: function(point) {
            var refreshIntervalId
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);
            chart.redraw();
            // call it again after one second
            // setTimeout(requestData, 4000);
            $("#setinterval").change(function() {
                // clearInterval(refreshIntervalId);
                refreshIntervalId = setTimeout(requestData, this.value);
            });
            refreshIntervalId = setTimeout(requestData, 4000);
        },
        // cache: true
    });
}*/


$(document).ready(function() {
    chart = new Highcharts.Chart({
        boost: {
            allowForce:"true"
        },
        chart: {
            backgroundColor:"#FFFFFF",
            renderTo: 'host-cpu',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }

        },
        title: {
            text: 'CPU Host'


        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 100,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.5,
            maxPadding: 0.5,
            title: {
                text: 'CPU %',
                margin: 20
            }
        },
        series: [{
            name: 'Cpu Host',
            data: []
        }]
    });
});

$(document).ready(function() {
    chart1 = new Highcharts.Chart({
        chart: {
            renderTo: 'host-mem',
            defaultSeriesType: 'spline',
            events: {
                load: requestData1
            }

        },
        title: {
            text: 'Memory Host'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 100,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.5,
            maxPadding: 0.5,
            title: {
                text: 'Memmory %',
                margin: 20
            }
        },
        series: [{
            name: 'Memory host',
            data: []
        }]
    });
});
