$(document).ready(function () {
    $('#step-btn').click(function () {
        fetchStep();
    });

    $('#run-simulation-btn').click(function () {
        let intervalId = setInterval(() => {
            fetchStep();
            if (!isSimulationRunning) { // Variable to control running state
                clearInterval(intervalId);
            }
        }, 100); // Adjust time as needed for your simulation's speed
    });
});

let isSimulationRunning = true; // Control variable

function fetchStep() {
    $.ajax({
        url: '/step', // Modify with your actual endpoint
        method: 'GET',
        success: function (data) {
            updateStations(data.stations);
            updateTanker(data.tanker);
            updateMap(data);
        },
        error: function () {
            alert('Error fetching data.');
            isSimulationRunning = false; // Stop simulation on error
        }
    });
}


function updateTanker(tanker) {
    let tankerInfo = `<div class="card mb-2">
        <div class="card-body">
            <h5 class="card-title">Tanker Info</h5>
            <p class="card-text">Position: (${tanker.x.toFixed(2)}, ${tanker.y.toFixed(2)})</p>
            <p class="card-text">Capacity: ${tanker.capacity} liters</p>
            <p class="card-text">Current Load: ${tanker.current_load} liters</p>
            <p class="card-text">Target Station: ${tanker.target_station}</p>
        </div>
    </div>`;

    $('#tanker-info').html(tankerInfo); // Ensure you have a div with id="tanker-info" in your HTML
}

function updateStations(stations) {
    let stationsContainer = $('#stations-container');
    stationsContainer.empty(); // Clear previous entries

    stations.forEach(function (station) {
        let stationInfo = `<div class="card mb-2">
            <div class="card-body">
                <h5 class="card-title">Station at (${station.x}, ${station.y})</h5>
                <p class="card-text">Capacity: ${station.capacity} liters</p>
                <p class="card-text">Current Fuel: ${station.current_fuel} liters</p>
            </div>
        </div>`;
        stationsContainer.append(stationInfo);
    });
}

function updateMap(data) {
    var ctx = document.getElementById('map').getContext('2d');
    ctx.clearRect(0, 0, 800, 600); // Clear previous drawing

    var scale = 10; // Adjust this value to change the scale

    // Draw refuel center
    ctx.fillStyle = 'red';
    ctx.fillRect((data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale), 22, 22);
    ctx.fillText("Refuel Center", (data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale) - 10);

    // Draw stations
    data.stations.forEach((station, index) => {
        ctx.fillStyle = 'blue';
        ctx.fillRect((station.x * scale) + 400, 300 - (station.y * scale), 20, 20);
        ctx.fillText("Station " + (index + 1), (station.x * scale) + 400, 300 - (station.y * scale) - 10);
    });

    // Draw tanker
    ctx.fillStyle = 'green';
    ctx.fillRect((data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale), 22, 22);
    ctx.fillText("Tanker", (data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale) - 10);
}