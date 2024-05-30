# Gas Station Refuelling Simulation

This simulation models a gas station and the process of refuelling cars and the station's fuel tank. It uses the SimPy library for process-based discrete-event simulation.

![image](https://github.com/michalskibinski109/GasStationSimulation/assets/77834536/f87605dc-336c-4d6e-9763-31c665a6d81c)


## How it works

The simulation includes the following entities:

- **Cars**: Cars arrive at the gas station at random intervals. Each car has a fuel tank of a certain size and a current fuel level. When a car arrives at the gas station, it requests a refuelling process. The amount of fuel required is calculated, and the car waits for its turn to be refuelled.

- **Gas Station**: The gas station has a limited number of fuel pumps (resources) and a fuel tank with a certain capacity. When a car requests a refuelling process, the gas station checks if it has enough fuel in its tank to fulfil the request. If not, it triggers a process to call a tank truck.

- **Tank Truck**: The tank truck is called when the fuel level at the gas station drops below a certain threshold. It takes a certain amount of time for the tank truck to arrive at the gas station. Once it arrives, it refills the gas station's tank to its full capacity.

The simulation runs for a specified amount of time. During this time, it logs events such as car arrivals, refuelling processes, and tank truck calls. It also collects data on the fuel level at the gas station at different points in time.

At the end of the simulation, it plots the fuel level at the gas station over time.

## Requirements

- Python 3.6+
- SimPy
- Matplotlib
- Rich

## Running the Simulation

To run the simulation, simply execute the `main.py` script:

```bash
python main.py
```
