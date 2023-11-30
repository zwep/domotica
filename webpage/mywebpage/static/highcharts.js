// Load the CSV file using AJAX
function loadCSV(callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            callback(xhr.responseText);
        }
    };
    xhr.open("GET", "/home/bugger/Documents/data/arduino/remote_sensor.csv", true);
    xhr.send();
}

// Parse the CSV data and create the chart
function createChart(csvData) {
    // Parse CSV data into an array
    var lines = csvData.split("\n");
    var data = [];
    for (var i = 1; i < lines.length; i++) {
        var parts = lines[i].split(",");
        var date = parts[0];
        var value = parseFloat(parts[1]);
        data.push([date, value]);
    }

    // Create the Highcharts chart
    Highcharts.chart('chartContainer', {
        title: {
            text: 'CSV Graph'
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Value'
            }
        },
        series: [{
            name: 'Value',
            data: data
        }]
    });
}

// Call the functions to load the CSV and create the chart
loadCSV(createChart);
