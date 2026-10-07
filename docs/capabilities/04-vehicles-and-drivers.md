# Vehicles and Drivers: What You Can Give a Vehicle

## A body and a personality

Every simulated vehicle is described by a type, and the type is where most of SUMO's expressive power lives. The attributes fall naturally into a body and a personality, plus a few that concern what the vehicle is for.

The **body** covers physical size and performance: length, width and height, mass, maximum speed, acceleration and deceleration, a separate emergency braking limit, and a shape for drawing, which can be a passenger car, delivery van, truck with trailer, bus, coach, tram, motorcycle, bicycle, pedestrian, ship, or a custom image or 3D model. The vehicle can have a colour, a name, a class, an emission model and a fuel type, an energy and battery specification, and a capacity for passengers and containers, with boarding and loading times. Trucks can have trailers modelled by adjusting length and mass as cargo is loaded, and vehicles can carry signals such as blinkers, brake lights, a blue light or hazard flashers, which are visible in the GUI and can be set from a script.

The **personality** covers how it drives. A driver has a desired time headway, a standing gap to the vehicle ahead, an imperfection level that produces random dawdling, a speed factor that decides whether the driver respects, exceeds or undercuts the limit, and an optional desired top speed. A driver may be more or less eager to change lane for strategic reasons, to gain speed, to keep right, to cooperate with others or to overtake on the right, may accept small gaps or insist on large ones, may become impatient as waiting time grows, may drive in the middle of a lane or on its right edge, may squeeze past neighbours laterally, may tolerate or ignore conflicting traffic at junctions with a given probability, may run a freshly changed red or yellow light, may stop further back from stop lines, may refuse to enter a blocked junction or insist on it after a wait, and may overtake through the oncoming lane. The decision interval of a driver can be coarser than the simulation step to model reaction time, and an optional driver-state model adds perception errors, situation awareness and reaction delays.

## Choosing a car-following model

SUMO is not tied to one theory of driving. The default Krauss model is a stochastic safe-speed model with a long record in the field, with a variant that accounts for slopes. Alternatives include the Intelligent Driver Model and its improved and extended versions with realistic acceleration profiles, a Wiedemann psycho-physical model of the kind used in commercial tools, adaptive and cooperative adaptive cruise-control models, models by Kerner and Wagner and others, and a dedicated rail model for trains with traction curves. Models can be mixed in one simulation, so that human drivers, adaptive-cruise vehicles and trains share the network. The lane-change side offers the default LC2013 and a sublane model with lateral dynamics, and parameters of both can be altered live.

## Heterogeneous fleets

Fleets are rarely uniform, and SUMO has several ways to say so. A vehicle type can be a **distribution** of types with probabilities, so that, say, nine tenths of vehicles are ordinary cars and one tenth are trucks with different dynamics. Numeric attributes can themselves be drawn from distributions: the speed factor has a normal distribution with optional truncation, and a generator can produce types whose parameters are sampled from ranges. Vehicles can be individually coloured, individually assigned to a route from a distribution, and equipped with devices at a chosen penetration rate, so that a sensor, rerouting capability, battery model or communication unit exists in, for example, thirty per cent of the fleet.

## Departure and arrival behaviour

A vehicle can be placed on a particular lane, a random lane, the emptiest lane or the best lane for its route, at a particular position, a random position or directly behind the previous vehicle, and at a given speed, a maximum speed, a random speed or the average speed of the road. It can wait for a person to trigger its departure, depart from a stop or parking space, and arrive on a chosen lane at a chosen position and speed, or arrive when it is simply removed. Time can be given in seconds or in clock format.

## Stops, waypoints and special behaviours

Vehicles can have stops along their route, at a lane position, a bus stop, a container stop, a parking area, a charging station or a train station, each with a minimum duration or a scheduled departure time, or with a trigger such as waiting for a person or container. A stop can be a **waypoint**, which only requires passing at a given speed. A vehicle can park off the road so as not to block traffic, can **jump** out of the network for a time and re-enter, can loop on a cyclic route with a cycle time, can repeat a route a number of times, and can have a line identifier and a destination sign so that persons and the intermodal router can recognise it as a public-transport service.

## Everything is a parameter

Any object can also carry free-form key-value parameters, which many features read to configure themselves, and every vehicle attribute can be queried and changed at runtime by a program driving the simulation. That includes the type parameters themselves, so that a vehicle's headway or lane-change eagerness can be adjusted in mid-run to model changing mood, automation levels or driver response to information.
