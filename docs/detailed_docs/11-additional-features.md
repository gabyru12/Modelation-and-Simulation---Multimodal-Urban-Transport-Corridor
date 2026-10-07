# Additional Features

## Devices as an extension mechanism

Many optional capabilities in SUMO are delivered as **devices**: small components that are attached to individual vehicles (or persons) and hook into their lifecycle, reading and sometimes changing their behaviour. A device is attached in one of three ways. It can be assigned by a global option such as `--device.rerouting.probability 0.3`, which equips a random share of the fleet, it can be assigned to listed vehicles with the corresponding `explicit` option, or it can be declared as a generic parameter on a vehicle or vehicle type. Because devices are opt-in and per vehicle, a scenario can mix equipped and unequipped vehicles at any penetration rate, which is exactly what is needed to study partial adoption of a technology. The built-in devices include emission, battery, stationfinder, electric hybrid, bluetooth sender and receiver, blue light, surrogate safety measures, take-over-control, driver state, floating-car data, trip information, route output, rerouting, taxi, GLOSA and friction.

## Emissions

Each vehicle type has an `emissionClass` of the form `model/class`, such as `HBEFA3/PC_G_EU4`. SUMO integrates several models: HBEFA in versions 2.1, 3.1 and 4.2, which give emission factors per vehicle category and driving state, and PHEMlight and PHEMlight5, which compute emissions from engine power demand derived from speed, acceleration and, when elevation is present, slope. A `Zero` class emits nothing, and electric classes consume electricity. The tracked quantities include carbon dioxide, carbon monoxide, hydrocarbons, nitrogen oxides, particulate matter, fuel and, for PHEM, electricity, together with a noise estimate. Since version 1.14 fuel is reported in milligrams instead of litres. Idle vehicles keep emitting, and the engine is automatically switched off after 300 seconds at a planned stop, while coasting vehicles are treated as having the engine off. Emissions can be written per vehicle and step, per edge and interval, or in trip information, and the GUI can colour vehicles and lanes by emission level. Two helper tools, `emissionsMap` and `emissionsDrivingCycle`, evaluate the models offline.

## Electric vehicles and hybrids

The electric vehicle model is implemented by the **battery device**. It integrates energy over time from a consumption model that depends on mass, speed, acceleration, aerodynamic drag, rolling resistance, slope and efficiency, with regeneration during braking, and it tracks the state of charge against a battery capacity (35 kilowatt-hours by default) with a limit on the charge rate. **Charging stations** are lane segments with a power, an efficiency and a mode, and a vehicle charges while stopped or in transit over one. The battery output records energy per step and the charging output records sessions. With a tracking option, the same device can model the fuel tank of a conventional vehicle.

The **stationfinder** device adds autonomy: it monitors the energy level, and once it drops below a threshold (40 per cent by default) searches for charging stations within a time radius, ranks candidates by travel time, charging time, waiting time and capacity, and reroutes to the best, charging up to a saturation level. If the battery falls near empty, a rescue action removes or tows the vehicle after a delay. **Electric hybrids** such as trolleybuses are modelled by traction substations, overhead wire segments and clamps that connect segments into circuits, with a vehicle device combining a battery with power drawn from the wire.

## Emergency vehicles

A vehicle equipped with the **blue-light device** receives privileges such as ignoring red signals and changing lanes freely when jammed. In the sublane model, surrounding vehicles that notice the emergency vehicle within a reaction distance (25 metres by default, with probabilities per second that depend on proximity) form a **rescue lane** by moving to the left or right edge of their lanes, depending on which lane they are in, and return to normal after it has passed.

## Taxis and demand-responsive transport

A vehicle becomes a taxi by carrying a taxi device. Customers either request a ride directly (`ride lines="taxi"`) or let the intermodal router choose taxi as a mode, optionally as groups or with pre-booking, and the dispatcher assigns taxis to reservations. Five algorithms are available: *greedy* assigns the closest taxi in order of requests, *greedyClosest* assigns the closest customer to each taxi, *greedyShared* allows ride-sharing under detour limits, *routeExtension* is a flexible pick-up algorithm for shared rides, and *traci* delegates dispatch to an external program through `getTaxiReservations`, `getTaxiFleet` and `dispatchTaxi`. Idle taxis can stop, circle randomly or queue at taxi stands, and trip information records customers served and occupancy.

## GLOSA, platooning and related assistance systems

**GLOSA**, the Green Light Optimal Speed Advisory device, lets a vehicle within communication range (100 metres by default) of a signal compute whether it would arrive during a red phase and, if so, reduce its speed factor so that it arrives at the start of green without stopping, or, if it would arrive at the end of green, raise its speed factor up to a maximum to pass in time. Newer versions can include the length of the queue at signals with delay-based detectors. **Simpla**, a Python plug-in built on TraCI, forms platoons spontaneously: vehicles within a gap threshold behind a leader join it and are assigned vehicle types for the roles of leader, follower, catch-up and catch-up follower, which change their car-following parameters, with limits on platoon size and a configurable control rate. Because simpla changes types, speed factors and lane-change modes, it should not be combined with other scripts that control the same properties. The **take-over-control** device, the **driver-state** device and the **surrogate-safety** device cover automation hand-over, perception imperfection and safety metrics such as time-to-collision.

## Generic parameters

Almost every object accepts arbitrary key-value pairs through `param` elements, which can be edited in netedit, read and written through TraCI, and are saved and restored with simulation state. They are used for both annotations and behaviour: they equip devices, configure actuated signals, set electric-vehicle properties and parking search, and tune emission models.

```xml
<vehicle id="v0" route="r0" depart="0">
  <param key="has.battery.device" value="true"/>
</vehicle>
```

## Shapes and wireless detection

Polygons and points of interest are drawn objects that exist for visual context and debugging, defined by identifier, shape or position (in Cartesian, lane or geographic coordinates), colour, layer and optional image. Wireless detection is modelled by a pair of devices, a **sender** that makes a vehicle or person detectable and a **receiver** that detects senders within a range, with an off-time between connections that models communication load, and an output file records each encounter with times, positions and speeds. Parked vehicles equipped as receivers represent roadside units, enabling vehicle-to-infrastructure studies.

## Logistics

Containers are transported by vehicles with a container capacity between container stops, and the stage elements for moving them are `transport` and `tranship`. The loading duration and the dynamic length and mass of trailers or rail cars allow models of ports and transhipment hubs.
