# Transport Modes and the People Who Use Them

## A palette of modes

SUMO describes a mode through the combination of a vehicle class, which fixes where it may travel, and a movement model, which fixes how. The built-in classes include passenger cars, taxis, buses, coaches, trucks and trailers, delivery vehicles, motorcycles and mopeds, bicycles, trams, urban rail, commuter and long-distance rail, ships, pedestrians, emergency vehicles, authority and military vehicles, vehicles with high occupancy, e-bikes and low-emission vehicles, and a special class that ignores restrictions. Each can be given its own lanes, its own speeds on shared roads, its own signal indications and its own parking and stopping facilities.

## Road vehicles

The great majority of the engine's machinery concerns road vehicles, and it supports an exceptional range of road situations: multi-lane motorways with ramps, weaving sections and variable speed limits; urban arterials with bus lanes and signalised junctions; roundabouts and unsignalised intersections of all priority types; rural roads with overtaking through the oncoming lane; parking behaviour including searching for free spaces; and junctions with pedestrians crossing. Heavy and light vehicles can have different speed limits and different allowed lanes, and vehicles can be stopped, parked, towed or removed at will.

## Public transport

Buses, trams and trains run on timetables, with lines, stops, dwell times, scheduled departure times and cyclic services. Passengers wait at stops, board vehicles that serve their line, and ride to their destination, with boarding times that depend on how many board. Timetables may be written by hand, imported from GTFS or derived from OSM public-transport relations, and the outcome can include delay, bunching and transfer failures. Transit signal priority, dedicated lanes and stop designs, such as bays and kerb extensions, can be tested by changing the network and control rather than the vehicles.

## Pedestrians

Pedestrians are fully fledged agents that walk on sidewalks, use crossings and walking areas and interact with vehicles and with each other. They may have different walking speeds, sizes, and start and end points anywhere on the network, may wait for a vehicle at a stop, and may share the movement area with bicycles in sublane mode. Three movement models trade speed against realism, from a non-interacting model to a lane-striped two-dimensional model and a JuPedSim coupling for crowds moving freely around obstacles in plazas, stations and event venues, including the handover between pedestrians and vehicles at drop-off points.

## Bicycles and micromobility

Bicycles can be simulated as slow, narrow vehicles that use bike lanes and share roads, with their own junction behaviour, lane alignment, speed and lateral movement, and also as fast persons. Because of the sublane model, bicycles can pass slower bicycles, filter through queued traffic, and ride beside cars in the same lane. E-bikes and mopeds exist as their own classes.

## Rail

Trains run on a track network with signals, switches and bidirectional segments, using a car-following model based on traction and resistance, with real-life train types such as freight and high-speed trains available as presets. Automatic block signalling prevents collisions and can enforce a train order, trains may reverse, join and split at stations, and large scenarios with timetables can be built from OSM and GTFS data. Trams share the road with traffic or run on their own tracks and obey the traffic signals.

## Ships and others

Ships can be simulated in waterways modelled as edges, which suit canals and rivers, with a dedicated class, shape and imports from OSM, although they use road-vehicle movement logic. Containers are also first-class objects that can be loaded onto, carried by and unloaded from vehicles at container stops, for logistics and port scenarios.

## On-demand and shared mobility

Taxis and demand-responsive transport can be simulated with customers requesting rides directly or via multimodal routing, with several dispatch strategies including ride-sharing, pre-bookings, groups, idle behaviours such as circling or queueing at taxi stands, and an interface for plugging in your own dispatcher. Persons can combine several modes in one chain, such as walk, bus, bike, walk, and the engine can compare the resulting mode choices.
