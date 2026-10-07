# Simulation

## Defining a simulation

A SUMO simulation is the combination of three kinds of input. The **network** is passed with `--net-file`. **Demand** is passed with `--route-files`, which accepts several files. **Additional files**, passed with `--additional-files`, describe everything else that is attached to the network: infrastructure such as bus stops, parking areas and detectors, control objects such as rerouters, calibrators and traffic-light programs, and visual objects such as polygons. These are usually gathered in a configuration file:

```xml
<configuration>
  <input>
    <net-file value="net.net.xml"/>
    <route-files value="routes.rou.xml"/>
    <additional-files value="stops.add.xml,detectors.add.xml"/>
  </input>
  <time><begin value="0"/><end value="3600"/><step-length value="1"/></time>
</configuration>
```

Loading order matters and explains many "unknown identifier" errors. The network is read first, then the additional files, completely and in the order given, then the route files, of which only the first few steps are opened. As the simulation proceeds, further portions of the route files are read incrementally. A type, route or stop that a vehicle refers to must therefore already exist when the vehicle is read, and additional files that define such things must precede the vehicles.

The run starts at `--begin` (default 0) and ends when `--end` is reached, when all vehicles have finished, or, under external control, when the client closes the connection. The temporal resolution is `--step-length`, a value between 0.001 and 1 seconds, with one second as the default. Smaller steps produce smoother motion and make insertions and lane changes more likely to succeed, but cost proportionally more computation, so a step of 0.1 seconds is roughly ten times slower. The position update uses an Euler scheme by default, which assumes constant speed within a step, and a ballistic scheme with constant acceleration is available through `--step-method.ballistic` and is more accurate for coarse steps. An important distinction is that between the *simulation step* and a vehicle's **action step length**: a vehicle can be configured to re-evaluate its driving decisions only every so many seconds, which models reaction delay without shrinking the global step, and doing so automatically switches integration to the ballistic method.

Other global options shape behaviour in the broad sense. `--scale` multiplies demand, `--seed` and `--random` control randomness, `--time-to-teleport` handles gridlocks, `--collision.action` decides what happens to colliding vehicles, `--lateral-resolution` activates the sublane model, `--mesosim` switches to the mesoscopic engine, and `--max-depart-delay` and `--max-num-vehicles` bound the insertion queue and the network population. The effects of these are explained in [12-model-details.md](12-model-details.md).

## Saving and loading state

A simulation can be frozen and resumed. States are written at fixed times with `--save-state.times`, periodically with `--save-state.period` (optionally keeping only the latest few snapshots with `--save-state.period.keep`), interactively from the GUI, or from a script with `traci.simulation.saveState`. File names follow a prefix-time-suffix pattern and are gzip-compressed by default. A state is restored with `--load-state`, normally using the same input files as the original run and a `--begin` equal to the saved time, and `--load-state.offset` shifts all stored times, for instance back to midnight, while `--load-state.remove-vehicles` drops chosen vehicles.

A state contains vehicle positions and runtime status. Optional switches add the random number generator state (about half a megabyte), persons and containers, and rail-signal constraints. The documentation is explicit about limits: flows are re-created from the original route files rather than stored, the internal state of lane-change and car-following models is not saved, and parking positions are only approximately preserved, so a resumed run is not guaranteed to be bit-identical to an uninterrupted one. Through TraCI, `load` reloads the entire simulation, whereas `simulation.loadState` is faster because it clears vehicles and persons while keeping the loaded network. Saving and loading is the standard way to run many what-if experiments from a common warmed-up traffic state, because the cost of building up congestion is paid once.

## The SUMO-JuPedSim coupling

SUMO's own pedestrian model is lane-based, which is sufficient for sidewalks and crossings but not for open plazas, station concourses or event venues where pedestrians move in any direction around obstacles. The coupling with **JuPedSim**, the pedestrian simulator of Forschungszentrum Jülich, adds exactly that. The pedestrians in a defined **walkable area** are simulated by JuPedSim at a fine time resolution of 0.01 seconds in a two-dimensional polygon that may contain holes for barriers, trees or pillars. Their positions are then mapped back into the SUMO network, with pedestrians outside any lane assigned to the nearest edge for consistency with outputs and TraCI.

Walkable areas can be imported from DXF drawings or drawn in netedit, or derived from existing pedestrian infrastructure. Further configuration covers the parameters of the CollisionFreeSpeedModel, speed adjustments in zones, spawn sources, transfer points where people change between vehicle and pedestrian, waypoints and exits, and vanishing zones that model exit capacity. The limitations stated in the manual are that only the collision-free speed model has been tested extensively, pedestrians do not yet react to vehicles, waiting behaviour at crossings is simplified, and the very small time step makes JuPedSim the runtime-limiting component. It is therefore worth enabling only where crowd dynamics and traffic interact, such as a station forecourt that spills onto a road.
