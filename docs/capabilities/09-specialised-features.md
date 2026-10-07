# Specialised Features

## Environment and energy

SUMO can attach an emission model to each vehicle type, choosing among the HBEFA generations and the PHEMlight engine-power models, with passenger cars, light and heavy duty vehicles, buses, motorcycles and electric classes, and with the pollutants carbon dioxide, carbon monoxide, hydrocarbons, nitrogen oxides, particulates, fuel use and electricity use, as well as a noise estimate. Idling, engine switch-off, coasting and slopes all feed into the numbers. Electric vehicles carry a battery with a capacity, charge rate and consumption model that depends on mass, speed, acceleration, drag and gradient, recuperate energy when braking, and charge at stations either at stops or while driving over charging infrastructure. The stationfinder lets vehicles notice low charge, choose a charging station by weighing travel time, charging time, waiting time and station capacity, and rescue stranded vehicles. Trolleybuses and other hybrids draw power from overhead wires fed by substations, and conventional vehicles can be given a fuel tank with the same device.

## Connected and automated driving

Adaptive and cooperative cruise-control models, platooning plug-ins that form and dissolve platoons dynamically with different behaviour for leaders, followers and catch-up vehicles, GLOSA devices that advise speeds to hit green lights and can account for queues, take-over-control devices that hand over between automated and manual driving, driver-state models that add perception errors and delays, and wireless sender and receiver devices form a toolkit for cooperative-driving research. The model for communication itself is delegated to co-simulators.

## Emergency and special operations

Emergency vehicles can use a blue-light device to ignore red signals and push through jams, and surrounding traffic in the sublane model forms a rescue lane in response. Vehicles can be broken down, stopped, parked on the road or towed, accidents can be created by blocking lanes, and rerouters and calibrators model the rest of the response.

## Safety analysis

Collision behaviour can be set from "teleport the follower" to "remove both vehicles", with options for how close counts as a collision and checks for overlap at junctions. Surrogate-safety devices record conflicts without them becoming crashes, which allows safety evaluation of designs and of automated-driving behaviours in a large number of virtual hours.

## Weather and surface

The friction model lets road grip vary by lane and time, reducing the speeds drivers choose with some perception noise, so that ice or rain on a stretch can be simulated or changed live.

## Logistics

Containers can be picked up and delivered between container stops, vehicles can change size and mass with the load, and port and rail-yard scenarios can be assembled from rail, road and container elements.

## Statistical and structural options

Demand can be scaled globally, fleets can be given random equipment, traffic can follow day profiles, vehicles can be removed when they wait too long or inserted with delay limits, gridlocks can be resolved by teleporting, and the network population can be capped. The engine can run a deterministic or a randomly seeded scenario, repeat it with different seeds, change step length for accuracy or speed, and switch integration methods.

## Beyond the obvious

Smaller capabilities add colour to the picture: routes with cyclic timetables, vehicles that wait for passengers, ships and trains on the same engine, stops that last until a given clock time, stops on the opposite side of the road, overtaking on the right with a given probability, junction heuristics tuned per vehicle, drawings of buildings, background images and 3D models, and custom data attached to nearly any object through generic parameters.
