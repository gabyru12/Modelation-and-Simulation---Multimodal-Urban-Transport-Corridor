# Live Control and Integration

## Steering a running simulation

The control interface, TraCI, gives an external program almost the same power as the simulation itself. Through a connection it can advance the clock a step at a time, read the state of any vehicle, person, lane, edge, junction, signal, detector, stop, parking area or charging station, and change much of that state. A script can add or remove vehicles and persons, change a vehicle's route, destination, speed, lane, lateral position, signals, colour and parameters, insert or alter stops, and teleport it to a new place. It can alter type parameters mid-run, close lanes, change speed limits and permissions, set friction, switch signal programs and phases, query routes and intermodal routes, convert between map, lane and geographic coordinates, and highlight objects in the GUI. A vehicle can be told to follow a speed or lane choice while the script decides how much of the vehicle's own safety logic to keep or override, so one can study anything from small nudges to total control.

Reading is as flexible as writing. Besides asking for single values, a program can subscribe to a set of variables and receive them automatically at each step, or subscribe to every object within a range of a reference object, as a connected vehicle would sense its surroundings, with server-side filters by lane, class or field of view. Information that comes from the driver model itself, such as the safe speed behind a leader, the safe gap, the leader and its distance, upcoming signals and their phases, junction foes and upcoming lane-change possibilities, can be queried, which makes it easy to build assistance systems on top.

## Ways to connect

The same interface exists as a socket protocol and as an in-process library. The socket version lets programs written in any language talk to SUMO, run on another computer, or share a simulation among several clients that are kept in lockstep. The in-process library, libsumo, trades those options for speed, since no messages cross a socket, and can be used from Python, C++, Java and, experimentally, C# and MATLAB. A compatible variant combines the library's API with the socket protocol. Several simulations can be controlled from one program using labelled connections.

## Applications built on the interface

The interface is the basis of an entire family of uses. Adaptive and learning signal controllers, ramp metering and variable-message-sign logic can be written in a few dozen lines. Platooning, cooperative driving and automated-driving hand-over can be implemented by changing vehicle parameters and speeds. Taxi and shuttle fleets can be dispatched by an external algorithm. Co-simulations couple SUMO with network simulators for vehicular communication, with vehicle dynamics simulators, with driving simulators and with hardware in the loop, with SUMO providing the traffic and the other simulator providing the other half. Reinforcement-learning frameworks wrap it as an environment. Vehicles can be moved to externally supplied positions, which allows replaying or mirroring measured traffic.

## Save, restore and branch

A running simulation can be saved to a file at specific times or at intervals and restored later, optionally with the random generator state and the persons and containers. This enables warm starts, in which the costly build-up of congestion is done once, as well as branching experiments, in which many control strategies are tested from the same traffic situation, checkpointing of long runs, and fast resets in learning loops.

## Crowd simulation coupling

Pedestrian crowd dynamics in complex areas can be delegated to the JuPedSim simulator, which treats pedestrians as continuous-space agents among obstacles and exchanges them with SUMO at defined transfer points, so that passengers leaving a train, crossing a road or boarding a bus interact with both worlds.

## Data in and out

Because every file is XML, and because many outputs can also be written as CSV or Parquet, SUMO fits naturally into analysis pipelines: scripts can generate input files in bulk, run batches in parallel with different seeds or parameters, collect results into data frames and plot them with the supplied visualisation tools or any other library.
