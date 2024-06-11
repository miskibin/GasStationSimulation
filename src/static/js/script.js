$(document).ready(function () {
    $('#step-btn').click(function () {
        fetchStep();
    });


    $('#run-simulation-btn').click(function () {
        if (isSimulationRunning) {
            $(this).text('Run Simulation');
            isSimulationRunning = false;
        } else {
            $(this).text('Stop Simulation');
            isSimulationRunning = true;
            let simulationTime = $('#simulation-time').val(); // Fetch simulation time from input field
            let intervalId = setInterval(() => {
                if (!isSimulationRunning) {
                    clearInterval(intervalId);
                } else {
                    fetchStep();
                }
            }, simulationTime); // Use simulation time for interval
        }
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
    let loadPercentage = (tanker.current_load / tanker.capacity) * 100;

    let tankerInfo = `<div class="card mb-2">
        <div class="card-body">
            <h5 class="card-title">Tanker Info</h5>
            <p class="card-text">Position: (${tanker.x.toFixed(2)}, ${tanker.y.toFixed(2)})</p>
            <p class="card-text">Capacity: ${tanker.capacity} liters</p>
            <p class="card-text">Current Load: ${tanker.current_load} liters</p>
            <p class="card-text">Target Station: ${tanker.target_station}</p>
            <div class="progress">
                <div class="progress-bar" role="progressbar" style="width: ${loadPercentage}%" aria-valuenow="${loadPercentage}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
        </div>
    </div>`;

    $('#tanker-info').html(tankerInfo);
}

function updateStations(stations) {
    let controlContainer = $('#tanker-control-container');
    controlContainer.empty();
    let stationsContainer = $('#stations-container');
    stationsContainer.empty();

    stations.forEach(function (station) {
        let fuelPercentage = (station.current_fuel / station.capacity) * 100;
        let refuelingBadge = station.is_refueling_car ? '<span class="badge text-primary mx-2 my-0 px-2 py-0">Currently Refueling Car</span>' : '';

        let stationInfo = `<div class="card mb-2">
            <div class="card-body">
                <h5 class="card-title">Station at (${station.x}, ${station.y}) ${refuelingBadge}</h5>
                <p class="card-text">Capacity: ${station.capacity} liters</p>
                <p class="card-text">Current Fuel: ${station.current_fuel} liters</p>
                <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: ${fuelPercentage}%" aria-valuenow="${fuelPercentage}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>`;
        stationsContainer.append(stationInfo);
        let controlButton = $(`<button class="btn btn-primary m-2" data-destination="${station.x},${station.y}">Go to Station at (${station.x}, ${station.y})</button>`);
        controlButton.click(function () {
            let destination = $(this).data('destination');
            $.ajax({
                url: `/set_tanker_destination/${destination}`,
                method: 'GET',
                success: function (response) {
                    console.log(response);
                },
                error: function () {
                    alert('Error setting destination.');
                }
            });
        });
        controlContainer.append(controlButton);

    });
}


function updateMap(data) {
    var ctx = document.getElementById('map').getContext('2d');
    ctx.clearRect(0, 0, 800, 600); // Clear previous drawing

    var scale = 10; // Adjust this value to change the scale

    // Draw refuel center
    ctx.fillStyle = 'green';
    ctx.fillRect((data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale), 22, 22);
    ctx.fillText("Refuel Center", (data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale) - 10);

    // Draw stations
    data.stations.forEach((station, index) => {
        ctx.fillStyle = station.current_fuel > 0 ? 'blue' : 'red';
        ctx.fillRect((station.x * scale) + 400, 300 - (station.y * scale), 20, 20);
        ctx.fillText("Station " + (index + 1), (station.x * scale) + 400, 300 - (station.y * scale) - 10);
    });

    // Draw tanker
    ctx.fillStyle = 'purple';
    ctx.fillRect((data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale), 22, 22);
    ctx.fillText("Tanker", (data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale) - 10);
}


