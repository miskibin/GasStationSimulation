var isSimulationRunning = true; // Control variable
const stationImage = new Image();
stationImage.src = 'static/image/station.png';
$(document).ready(() => {
    $('#step-btn').click(fetchStep);

    $('#run-simulation-btn').click(toggleSimulation);
});

function toggleSimulation() {
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
}

function fetchStep() {
    $.ajax({
        url: '/step', // Modify with your actual endpoint
        method: 'GET',
        success: handleFetchSuccess,
        error: handleFetchError
    });
}

function handleFetchSuccess(data) {
    updateStations(data.stations);
    updateTanker(data.tanker);
    updateMap(data);

    // Extract losses from stations and update total loss
    const lossPerStation = data.stations.map(station => station.loss);
    updateLoss(lossPerStation);
}

function handleFetchError() {
    alert('Error fetching data.');
    isSimulationRunning = false; // Stop simulation on error
}
function updateTanker(tanker) {
    const loadPercentage = (tanker.current_load / tanker.capacity) * 100;

    const tankerInfo = `
    <div class="card mb-2">
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
    const controlContainer = $('#tanker-control-container');
    controlContainer.empty();
    const stationsContainer = $('#stations-container');
    stationsContainer.empty();
    stations.forEach(station => {
        const fuelPercentage = (station.current_fuel / station.capacity) * 100;
        const refuelingBadge = station.is_refueling_car ? '<span class="badge text-primary mx-2 my-0 px-2 py-0">Refueling Car</span>' : '';

        const stationInfo = `
        <div class="card mb-2">
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
        const controlButton = $(`<button class="btn btn-primary m-2" data-destination="${station.x},${station.y}">Go to Station(${station.x}, ${station.y})</button>`);
        controlButton.click(createDestinationSetter());
        controlContainer.append(controlButton);

    });
    const btn = $(`<button class="btn btn-info m-2" data-destination="0,0">Go to Refuel center </button>`);
    btn.click(createDestinationSetter());
    controlContainer.append(btn);
}


function createDestinationSetter() {
    return function () {
        const destination = $(this).data('destination');
        $.ajax({
            url: `/set_tanker_destination/${destination}`,
            method: 'GET',
            success: response => console.log(response),
            error: () => alert('Error setting destination.')
        });
    };
}
function updateMap(data) {
    const ctx = document.getElementById('map').getContext('2d');
    ctx.clearRect(0, 0, 800, 600); // Clear previous drawing

    const scale = 10; // Adjust this value to change the scale

    // Load images
    const refuelCenterImage = new Image();
    refuelCenterImage.src = 'static/image/refuel_center.jpg'; // Ensure this path is correct
    const stationImage = new Image();
    stationImage.src = 'static/image/station.png'; // Ensure this path is correct
    const stationCar = new Image();
    stationCar.src = 'static/image/station_car.png'; // Ensure this path is correct
    const tankerImage = new Image();
    tankerImage.src = 'static/image/tanker.png'; // Ensure this path is correct
    refuelCenterImage.onload = () => {
        ctx.drawImage(refuelCenterImage, (data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale), 50, 50);
        ctx.fillText("Refuel Center", (data.refuel_center.x * scale) + 400, 300 - (data.refuel_center.y * scale) - 10);
    };
    stationImage.onload = stationCar.onload = () => {
        data.stations.forEach((station, index) => {
            // Choose the image based on whether the station is refueling a car
            const image = station.is_refueling_car ? stationCar : stationImage;
    
            ctx.drawImage(image, (station.x * scale) + 400, 300 - (station.y * scale), 40, 40);
            ctx.fillText(`Station ${station.x} ${station.y}` , (station.x * scale) + 400, 300 - (station.y * scale) - 10);
        });
    };

    tankerImage.onload = () => {
        ctx.drawImage(tankerImage, (data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale), 40, 40);
        ctx.fillText("Tanker", (data.tanker.x * scale) + 400, 300 - (data.tanker.y * scale) - 10);
    };
}
