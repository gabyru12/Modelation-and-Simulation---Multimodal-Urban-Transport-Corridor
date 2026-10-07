# Traffic Modes

## One engine, several kinds of mover

SUMO treats a *mode* as a combination of three things: a vehicle class that controls where the mover may go, a movement model that controls how it moves, and a set of network facilities that suit it. Cars, buses, trucks, motorcycles and taxis share the lane-based microscopic model with different parameters. Pedestrians use a separate person model, bicycles are slow vehicles with special parameters, trains use a dedicated car-following model together with signalling, and ships reuse the road-vehicle model with limited adaptation. Understanding which mode reuses which machinery tells you what to expect from its fidelity.

## Pedestrians

Walking is modelled as a person stage rather than as a vehicle. The network supports it through three infrastructure types. A **sidewalk** is a lane that permits only the pedestrian class, normally the right-most lane of an edge. A **crossing** links sidewalks across a road at a junction and is subject to the junction's right of way, and a **walking area** is the part of a junction where pedestrians pass from one sidewalk or crossing to the next. These can be imported from OpenStreetMap, guessed from road speeds (`--sidewalks.guess`), derived from permissions, or drawn in netedit.

Three movement models are available through `--pedestrian.model`. The default **striping** model assigns each pedestrian a two-dimensional position on a lane, divides the lateral width into narrow stripes of about 0.65 metres and avoids collisions by keeping enough distance within a stripe, which is cheap and reproduces counter-flows and overtaking plausibly. It includes anti-jam mechanisms, such as reserving space for oncoming flow and letting persistently stuck pedestrians continue at reduced speed after a timeout. The **non-interacting** model gives pedestrians fixed walking times without mutual interaction, which is very fast but unrealistic, and the **JuPedSim** coupling provides continuous-space crowd dynamics, as explained in [04-simulation.md](04-simulation.md). Default pedestrian speed is 1.39 metres per second with individual variation. Pedestrian demand comes from explicit person definitions, from `randomTrips.py --pedestrians`, from OD matrices, or from intermodal routing.

## Bicycles

Bicycles are simulated as vehicles of class `bicycle`, with a default length of 1.6 metres, a desired speed of 20 kilometres per hour and a smaller minimum gap, which makes them behave as slow, narrow vehicles in the same lane model as cars. Realistic cycling needs a few adjustments that the manual recommends: aligning bicycles to the right of the lane, reducing their eagerness for strategic lane changes, and lowering the crossing gap at junctions so that they cross more assertively, with `desiredMaxSpeed` set below `maxSpeed` if slope effects under KraussPS are wanted. Bike lanes are normal lanes that permit only the bicycle class and can be generated from typemaps, from `--bikelanes.guess` or in netedit. Known limitations include the lack of bidirectional movement on bike lanes and, without the sublane model, the impossibility of overtaking within a lane or sharing space with pedestrians. The sublane model resolves most of these because bicycles can then ride beside each other and beside cars.

## Railways

Rail simulation uses the same network graph with tracks as edges of rail classes (tram, subway, light rail, rail, high-speed), and parallel tracks are separate edges rather than lanes. Bidirectional tracks are modelled as two superposed edges with opposite geometries, and signals control which direction is in use. The `Rail` car-following model describes trains through traction and resistance curves, with predefined types, accounts for curve resistance, and considers train length when limiting speed and occupying blocks. **Rail signals** implement automatic block signalling in three protective functions: they prevent rear-end collisions within a block, flanking collisions at switches and head-on collisions on bidirectional sections, and they can also impose train order through constraints derived from timetables. Trains can reverse on bidirectional track, and portion working lets trains split and join at stops. Railway deadlocks are reported as a separate teleport reason.

## Waterways

Ships have the vehicle class `ship`, drawn with a ship shape, and a network of waterways is imported from OSM with the ship typemap or created by allowing the ship class on edges. SUMO has no dedicated ship movement model; it repurposes the road-vehicle algorithms, junctions on waterways default to unregulated, ships cannot reverse, and all movement must follow edges, so open-water navigation is possible only through TraCI. Overtaking requires several lanes, a wide lane with the sublane model, or opposite-direction driving.

## Choosing a representation

The decision between modes is practical. Where interactions between modes at conflict points matter, the lane-based vehicle model plus the striping pedestrian model is the standard combination. Where crowd density is the question, JuPedSim is needed. Where signalling constraints dominate, the rail model is irreplaceable, and where only the movement of a few boats is needed, TraCI-scripted ships are acceptable.
