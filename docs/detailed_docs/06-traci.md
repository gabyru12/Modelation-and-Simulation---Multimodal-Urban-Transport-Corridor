# TraCI: Online Interaction with a Running Simulation

## The idea

TraCI, the *Traffic Control Interface*, turns SUMO from a batch program into an interactive one. Instead of fixing everything in input files, an external program connects to a running simulation, advances it, reads the state of any simulated object, and changes that state. This is how adaptive traffic-signal controllers, connected-vehicle applications, dispatchers for taxi fleets, co-simulations with network or vehicle simulators and reinforcement-learning environments are built on top of SUMO.

The architecture is a TCP client/server pair in which **SUMO is the server**. It is started with `--remote-port PORT` and, rather than simulating, waits for a client to connect and take control. Several clients can share one simulation when started with `--num-clients N`. Each client receives an integer order, commands are processed in ascending order of that integer within a step, and the simulation advances only once every client has issued its step command, so clients are synchronised automatically after each step. When running under TraCI the `--end` option is ignored and the client decides when to finish by closing the connection, which is why scripts commonly loop while `getMinExpectedNumber()` is positive, meaning there are still vehicles loaded or running.

## What the interface exposes

The commands are organised into **domains**, one per kind of object. Traffic objects are vehicles, persons, routes and vehicle types. Network objects are edges, lanes, junctions and traffic lights. Infrastructure and detectors include induction loops, lane-area and multi-entry-exit detectors, bus stops, charging stations, parking areas and rerouters. Miscellaneous domains cover simulation-wide queries, the GUI, points of interest and polygons. Within each domain, commands fall into three kinds.

**Value retrieval** reads state. For vehicles this includes motion (speed, acceleration, lateral speed, angle, position in Cartesian and lane coordinates, distance driven, slope), route and network position (current edge and lane, route, route index, upcoming links), static properties (type, length, width, class, maximum speed, acceleration, deceleration, headway, imperfection, minimum gap), interactions (the leader and the gap to it, next traffic lights with distance and state, lane-change feasibility, neighbouring vehicles, junction foes, upcoming stops) and measured quantities (waiting time, time loss, emissions, fuel and electricity consumption, noise). It also exposes quantities derived from the car-following model such as the safe speed behind a leader, the safe gap and the speed that allows stopping at a given distance. The simulation domain adds time, step length, lists and counts of vehicles that loaded, departed, arrived, teleported or collided in the last step, network bounds, coordinate conversions between network and geographic systems, distance calculations, and route search through `findRoute` and `findIntermodalRoute`. Traffic-light getters return the current state string, phase index, program, remaining and elapsed durations, controlled lanes and links.

**State changing** modifies the world. For vehicles the key commands are `setSpeed`, which makes the vehicle drive at a given speed subject to its speed mode and reverts with a value of minus one, `slowDown`, which ramps to a speed over a duration, `setAcceleration`, `changeLane`, which requests a lane for a duration, `changeSublane`, `setRoute`, `changeTarget` (which recomputes the route to a new destination), `setStop`, `moveTo` and `moveToXY` for teleporting, `setSignals`, `setParameter` for model parameters, and rerouting commands based on travel time or effort. For traffic lights the main commands set the phase, the duration of the current phase, a complete red-yellow-green state string (which suspends automatic control), or a whole program. Edges and lanes accept new maximum speeds, permissions and travel-time weights, and a lane's friction coefficient can be changed during the run.

**Subscriptions** are the efficient alternative to polling. A client asks once for a list of variables for an object and receives them automatically after every step. **Context subscriptions** deliver the same variables for all objects within a range of a reference object, such as all vehicles within 100 metres of an ego vehicle, with server-side filters to reduce the volume. The documentation's benchmark of 9,000 vehicles over 5,000 steps showed subscriptions roughly halving the time of equivalent polling. A vehicle subscription ends automatically when the vehicle leaves the network.

## Overriding the driver: speed mode and lane-change mode

When a script commands a vehicle, it is competing with the vehicle's own driver model, and two bitsets say who wins. The **speed mode** is a bitset in which separate bits make the vehicle respect or ignore the safe speed to the leader, the maximum acceleration, the maximum deceleration, the right of way at intersections, braking for red lights, and finally the speed limit. The default value enables all safety checks, a value of zero disables almost all of them, and a value that clears every bit lets the commanded speed override everything, which may produce collisions or red-light running. The **lane-change mode** is a bitset in which pairs of bits set, for each of the lane-change motivations (strategic, cooperative, speed gain, keep right) and for sublane changes, whether the automatic model is disabled, allowed when it does not conflict with the TraCI request, or allowed to override it, and a further pair decides how strictly safety with other vehicles is respected. These two bitsets are the main control knobs for experiments in which an external controller should dominate, for example forcing a platoon speed, versus experiments in which it should merely nudge.

## Typical script structure

In Python the lifecycle is always the same: start or connect, loop on `simulationStep`, interleave reads and writes, and close.

```python
import os, sys
sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
import traci

traci.start(["sumo", "-c", "scenario.sumocfg"])
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for vid in traci.vehicle.getIDList():
        if traci.vehicle.getSpeed(vid) < 0.1:
            traci.vehicle.setColor(vid, (255, 0, 0, 255))
traci.close()
```

`traci.start` launches SUMO on a free port and connects. Passing a `label` creates named connections so that several simulations can run in parallel and be selected with `switch` or `getConnection`. Errors such as an unknown vehicle identifier surface as `traci.TraCIException`, which scripts should handle for objects that may have just left. All timing is in steps: nothing in the simulation moves between two `simulationStep` calls, so commands issued in that gap take effect in the next step. The `sumolib` helper library complements TraCI by reading the network and parsing output files offline.

Further TraCI facilities include saving and loading state mid-run, retrieving generic key-value parameters, drawing points and polygons, controlling the GUI view, and, for performance, replacing the socket by an in-process binding. That binding is the subject of [07-libsumo.md](07-libsumo.md).
