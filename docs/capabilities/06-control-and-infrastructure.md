# Traffic Control and Infrastructure

## Signals

SUMO supports traffic lights with fixed-time plans, with actuated control that extends greens while detectors see demand, with delay-based control that reacts to accumulated delay, and with controllers modelled on the American NEMA standard. Plans can have several programs per intersection, with offsets for coordination, switching at times of day, optional or skipped phases, flexible phase sequences, and expressions that use detector counts or gaps for custom rules. Signals can be switched off to fall back to priority rules. Joined signals can control several junctions as a single controller, and an external program can set the phase, the duration of the current phase, a complete state or an entirely new program while the simulation is running, which makes adaptive control, green waves, transit priority and reinforcement-learning controllers possible without changing the engine. Signal indications include green with and without priority, yellow, red, red-yellow, stop-then-turn and off states, and vehicles react to them in a way that includes the possibility of running a red or yellow light.

Railways have their own signalling in the form of rail signals that guarantee block separation, protect switches and bidirectional sections and can enforce timetable order.

## Speed and lane management

Variable speed signs can change the speed limit on chosen lanes over time, so that incident-warning or congestion-based speed harmonisation can be tested. Calibrators go further: they can force flows to match measured values by removing or inserting vehicles, set the speed on a lane, and change the type of vehicles that pass, for instance to model a share of trucks that grows over the day. Lane and edge permissions can change during a run, so bus lanes can be switched on and off, lanes closed for incidents, or reversible lanes created. Vaporizers remove vehicles at the end of an edge, which is helpful for sinks.

## Information and rerouting

Rerouters model information provision and incidents. They can close roads or lanes for all or some vehicle classes during given intervals, redirect vehicles to alternative destinations or predefined routes with given probabilities, and divert drivers to other parking areas when one is full. Compliance can be partial, so that only some drivers heed a sign, and vehicles with the rerouting device respond to congestion on their own.

## Stops, stations and parking

Bus stops, tram and train stops and container stops are placed on lanes with a length, capacity and optional access paths. Parking areas can be roadside bays or lots with individually placed and angled spaces, entry and exit manoeuvre times, capacity-based rerouting, and access control by permits. Charging stations deliver power to electric vehicles at a given rate and efficiency, and overhead wires, substations and clamps can power trolleybuses and hybrid vehicles.

## Detectors

Simulated sensors reproduce real measurement equipment. Induction loops count vehicles and measure speeds and occupancy at a point. Lane-area detectors measure occupancy, queue length and jam length over a segment, as a camera would. Multi-entry-exit detectors measure travel times across a zone. Route probes sample route shares, and the same measurement can be requested for whole edges and lanes. Detectors can feed actuated signals, be queried by a controlling program or be written to files to be compared with field data. Wireless detection is simulated with sender and receiver devices that log encounters, which allows vehicle-to-infrastructure scenarios.

## Visual and annotation objects

Points of interest and polygons can be drawn on the map to show buildings, land use or highlights, and objects can carry parameters shown in the GUI. The graphical interface can colour vehicles and lanes by almost any measure, follow vehicles, show detector values, record screenshots and videos, and replay saved traces.
