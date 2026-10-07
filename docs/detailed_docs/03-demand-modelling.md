# Demand Modelling

## Trips, routes and flows

Demand in SUMO is the set of movers that use the network, and it is described in **route files**. Three concepts form a ladder of specificity. A **trip** states only an origin edge, a destination edge and a departure time. A **route** is an expanded trip that lists every edge the vehicle will traverse, and the simulator requires routes in order to run. A **flow** is shorthand for many vehicles sharing the same origin, destination and type, emitted over a time window at a given rate. The distinction drives the whole toolchain: most demand-generation tools produce trips or flows, and a routing tool such as duarouter expands them into routes. SUMO can also accept trips directly and route them at insertion time, which is convenient but shifts the routing cost into the simulation.

Every simulated vehicle needs three things: a **vehicle type** (`vType`) that holds its physical and behavioural properties, a route, and a departure time.

```xml
<routes>
  <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="40"/>
  <route id="r0" edges="beg middle end"/>
  <vehicle id="v0" type="car" route="r0" depart="0"/>
  <flow id="f0" type="car" from="beg" to="end" begin="0" end="3600" vehsPerHour="600"/>
</routes>
```

The ordering rule is strict: types and named routes must be defined before the vehicles that reference them, and vehicles must be sorted by departure time, because the simulator reads the route file incrementally rather than loading it whole.

## Vehicle types and classes

A vehicle type bundles dozens of parameters. The kinematic ones are length, width, `maxSpeed`, acceleration `accel` and deceleration `decel`, with an `emergencyDecel` that is the hard physical braking limit. The behavioural ones are `tau`, the desired time headway, `minGap`, the standstill gap, `sigma`, driver imperfection, and the multiplier `speedFactor` with its deviation `speedDev`, which models drivers who consistently exceed or undershoot the limit. The `carFollowModel` attribute selects the longitudinal model, with Krauss as the default. The `vClass` attribute assigns the vehicle class, which determines which lanes it may use. Typical classes are passenger, taxi, bus, truck, bicycle, pedestrian, emergency, tram, rail and ship, and a type can additionally carry an emission class, a colour and lane-change and junction parameters that [08-driver-decision-making.md](08-driver-decision-making.md) describes in detail. Heterogeneous fleets are expressed with a `vTypeDistribution`, in which each member type has a probability, and a vehicle that references the distribution is assigned one member at random. A distribution of routes works the same way. A type with the special identifier `DEFAULT_VEHTYPE` redefines the defaults for every type that does not set a value.

Speed variation across a fleet is typically expressed as a distribution, for example `speedFactor="normc(1.0,0.1,0.2,2.0)"`, meaning a normal distribution with mean one, deviation 0.1, truncated to the interval 0.2 to 2.

## Departure, arrival and stops

A vehicle's departure is more than a time. `depart` may be a number, a clock string or `triggered` (waiting for a person to board), and `departLane`, `departPos` and `departSpeed` choose where and how fast the vehicle enters. Values such as `best`, `free`, `random`, `last`, `max` and `avg` let the simulator pick placements that maximise insertion capacity, and [12-model-details.md](12-model-details.md) explains why that matters. Arrival attributes control the exit lane, position and speed in the same way. A vehicle can be given waypoints (`via` edges) and **stops**, which are elements saying where and how long the vehicle waits. A stop can be on a lane at a position, at a named facility such as a bus stop or parking area, can be bounded by a `duration` or an `until` clock time, and can be `triggered` by a person or container. A stop with a positive speed becomes a waypoint, and a `jump` lets the vehicle leave the network for a time and re-enter at the next edge.

## Public transport

Public transport is built from ordinary vehicles with stops. A **bus stop** is infrastructure defined in an additional file as a lane segment with an identifier and the lines that serve it; train stops and container stops are analogues. A bus or tram refers to a stop in its route and waits for its `duration`. The `until` attribute gives schedule semantics, because a vehicle may not leave a stop before that time, although it can be late if traffic delays it. The meaning of `until` depends on context: absolute simulation time for a single vehicle, shifted per vehicle in a flow, relative to departure for a standalone route, and shifted by a cycle time for looped routes. Vehicles carry a `line` attribute so that persons and the intermodal router can match them to journeys. Complete public-transport data can be imported from GTFS timetables with `gtfs2pt.py`, which maps stops and routes onto a SUMO network, optionally guided by OSM route relations, and writes an additional file with stops and a route file with scheduled vehicles.

## Persons and trip chains

Besides vehicles, SUMO simulates **persons** who walk and ride. A person has a `depart` time and a *plan* consisting of stages: `walk`, which moves along edges or between points, `ride`, which boards a vehicle of a named line and rides to a destination, and `stop`, an activity of given duration. Positions carry over between stages, so only the first stage needs an origin.

```xml
<person id="p" depart="0">
  <walk edges="a b c"/>
  <ride lines="bus1" to="d"/>
  <walk from="d" to="e"/>
</person>
```

A `personFlow` creates many persons with the same plan. At a higher level a `personTrip` specifies only origin, destination and permitted modes, and the intermodal router fills in the walking, riding and waiting stages. Persons can start inside a vehicle by using `depart="triggered"`. Containers extend the same idea to freight, with container stops, `transport` and `tranship` stages, and loading and unloading durations; a vehicle that loads containers can change its length, mass and class, which may even force a reroute.

## Routing

The route computation is separate from the simulation and is performed by `duarouter`. Given trips, it computes least-cost routes on the network using, by default, the free-flow travel time derived from edge length and speed limit. The cost basis can be changed with weight files of measured or previously simulated travel times, and the tool supports routing between junctions, between traffic analysis zones, and between coordinates through map matching. Its options repair broken routes, ignore errors and convert flows to trips. The routing algorithm is selectable: Dijkstra is the exact default and supports every feature but is the slowest, A\* and its landmark-accelerated ALT variant speed up point-to-point queries, Contraction Hierarchies precompute a structure that makes huge numbers of queries cheap but cannot handle time-dependent weights without rebuilding, a wrapper variant maintains one hierarchy per vehicle class for multimodal networks, and customizable contraction hierarchies separate topology from weights so that frequent weight updates remain affordable.

**Intermodal routing** extends this to persons. Walking is always available, with a walk factor (default 0.75) discounting the nominal speed for interactions at crossings; cars, bicycles and taxis require a suitable vehicle type or mode; public transport requires vehicles with a `line`. Transfer points between modes are restricted to infrastructure such as parking areas and stops, and the cost combines vehicle travel times, scaled walking time, waiting for services and access distance.

Naive routing has a known flaw: if every driver takes the fastest path computed on an empty network, they all converge on the same bottleneck. **Dynamic user assignment** addresses this iteratively. The script `duaIterate.py` alternates between duarouter, which computes routes from current costs, and sumo, which simulates and measures new travel times, and each iteration shifts a share of the drivers between alternatives. The default Gawron model updates route probabilities from the previous probabilities and costs of the alternatives, damped by a parameter beta, while the logit model uses current costs only and can oscillate unless convergence steps are enforced. The goal is a user equilibrium in which no driver can improve their own travel time by switching route. A lighter alternative is **in-simulation rerouting** through the rerouting device, which lets vehicles recompute routes during the run at a configurable period using exponentially averaged or moving-average edge speeds, with options for traffic analysis zones, improvement thresholds, random distortion of weights and multithreading. Both approaches are complemented by rerouter objects and TraCI commands described elsewhere.

## Data sources for demand

Real demand data rarely arrives as vehicle lists, so SUMO ships importers for the usual forms. **Origin-destination matrices** are converted by `od2trips`, which reads VISUM-style V and O formats, the XML `tazRelation` format created and edited in netedit, and the Amitran format, together with a definition of traffic analysis zones (TAZ) that maps each zone to its edges with weights for departing and arriving traffic. Options scale the matrix, split it over time periods with a timeline or a daily profile, assign a type and add identifier prefixes so that repeated runs do not collide.

**Counting data** is handled by several tools. `dfrouter` and its refinement `flowrouter` derive routes and flows from detector definitions and CSV counts, and work best on motorway-like networks where all entries and exits are measured. `routeSampler.py` takes the inverse approach: given a pool of plausible routes, it selects a combination that reproduces observed edge counts and turn counts. `jtrrouter` needs no destinations at all, because it routes by **turning probabilities**: flows give only an origin edge, a turn-definition file gives the probability of each successor edge per interval, and vehicles leave when they reach a sink edge. Helper scripts generate turn definitions from the network or from existing routes. **Activity-based generation** with `activitygen` builds trips from a statistical description of a city's population (age brackets, employment, car ownership), its workplaces, schools and bus stations, and its gates for through-traffic, covering commuting, leisure and external trips by foot, bus or private car.

When no data exist, `randomTrips.py` produces random trips between edges chosen uniformly or by weights such as length, lane count or speed. A fringe factor raises the probability that trips start and end at the network boundary to mimic through-traffic, period and insertion-rate options control volume, the script can generate typed vehicles for buses or pedestrians, and an option calls duarouter to discard disconnected trips. Random demand is quick but unrealistic, and is best used for smoke tests and for multi-modal random traffic as in the web wizard. Finally, `createVehTypeDistribution.py` builds fleet distributions with sampled parameters, and netedit's demand mode lets one define trips, flows, routes, persons and stops graphically.
