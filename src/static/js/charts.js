const STATION_COUNT = 3; // This is hardcoded, ensure it matches the number of stations dynamically if needed.
console.warn('STATION_COUNT: IT IS HARDCODED!!!!', STATION_COUNT);
Chart.defaults.backgroundColor = $(':root').css('--bs-primary');
Chart.defaults.color = $(':root').css('--bs-light');
Chart.defaults.aspectRatio = 1.3;
Chart.defaults.plugins.legend.display = false;
Chart.defaults.plugins.title.font.size = 20;
Chart.defaults.plugins.title.display = true;
let totalLoss = [0];
let lossPerStation = [0, 0, 0];
let totalLossChart;
let stationLossChart;

let updateLoss = function (newLossPerStation) {
    if (newLossPerStation.length !== STATION_COUNT) {
        console.error("Mismatched station count and loss array length");
        return;
    }

    // Calculate total loss
    let newTotalLoss = newLossPerStation.reduce((acc, loss) => acc + loss, 0);
    totalLoss.push(newTotalLoss);

    // Update loss per station
    lossPerStation = newLossPerStation;

    console.log('totalLoss', totalLoss);
    console.log('lossPerStation', lossPerStation);

    // Create or update total loss line chart
    if (!totalLossChart) {
        let ctx = document.getElementById('totalLossChart').getContext('2d');
        totalLossChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({ length: totalLoss.length }, (_, i) => i),
                datasets: [{ label: 'Total Loss', data: totalLoss }]
            },
            options: {
                scales: { y: { beginAtZero: true } },
                plugins: {
                    title: {
                        display: true,
                        text: 'Total Loss Over Time'
                    }
                }
            }
        });
    } else {
        totalLossChart.data.labels = Array.from({ length: totalLoss.length }, (_, i) => i);
        totalLossChart.data.datasets[0].data = totalLoss;
        totalLossChart.update();
    }

    // Create or update station loss bar chart
    // Initialize or update the station loss chart
    if (!stationLossChart) {
        let ctx = document.getElementById('stationLossChart').getContext('2d');
        stationLossChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Array.from({ length: STATION_COUNT }, (_, i) => `Station ${i + 1}`),
                datasets: [{
                    label: 'Loss per Station',
                    data: lossPerStation, // Directly use the lossPerStation array
                }]
            },
            options: {
                scales: { y: { beginAtZero: true } },
                plugins: {
                    title: {
                        display: true,
                        text: 'Loss per Station'
                    }
                }
            }
        });
    } else {
        // Update the data for the dataset
        stationLossChart.data.datasets[0].data = lossPerStation;
        stationLossChart.update();
    }

};
