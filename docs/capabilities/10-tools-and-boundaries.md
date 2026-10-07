# Tools and Boundaries

## The toolbox around the engine

Around the simulator sits a workshop of programs. Netedit edits networks, demand and data graphically. Netconvert imports, merges, repairs and exports networks, and netgenerate makes abstract ones. The routers cover trips, turning ratios, detector counts and macroscopic assignment, and od2trips, activitygen and the route sampler cover matrices, populations and counts. A web wizard makes scenarios from a map in minutes, GTFS and OSM public-transport importers bring in schedules, polyconvert brings in buildings and land use, and scripts help to download large areas in tiles. Sumolib lets Python programs read networks and parse outputs, and the xml, visualisation, network, route, turn-count, trace-export, signal and emission tools handle post-processing. A few of these are worth singling out: a tool that compares two networks and produces a patch, one that builds vehicle-type distributions, one that checks network connectivity, and one that repeats a run under many seeds.

## The learning curve

Tutorials start from a first network in the editor and progress through importing real maps, controlling signals with a script, building railway scenarios and using JuPedSim. A very large reference of options and XML elements, a glossary, a change log, a FAQ and a growing body of conference material complete the picture, and the user community is active.

## What SUMO does not do, or does only approximately

An honest map includes its edges. SUMO does not model wireless communication itself, only the presence of devices, and it relies on co-simulation for network effects. It has no explicit model of weather beyond friction, nor of driver demographics beyond parameters, nor of parking pricing and economics. Its ship model borrows road-vehicle movement, and open-water navigation is possible only by external control. Its collision handling is a convenience and not a crash physics model, and the documentation states that collision freedom is not guaranteed. Its pedestrians in the lane-based models do not move in arbitrary directions and the JuPedSim coupling, while powerful, does not yet react to vehicles. Mesoscopic mode gives up lane-level and sublane detail and some detector types for speed. Saved states do not carry every internal model variable, so resumed runs can differ slightly from uninterrupted runs. Cross-platform bit-for-bit reproducibility is not guaranteed where math libraries differ. Imported networks need checking, because map data are incomplete, and demand usually needs calibration, because no import tool knows how many people really drive where.

## Reading the boundaries as design guidance

These boundaries are mostly an invitation to couple, script or calibrate rather than reasons to look elsewhere. Communication can be handled by a network simulator, human factors can be approximated by parameters or by a driving simulator in the loop, demand can be calibrated against counts, and unusual behaviours can be implemented in a controlling program. For the great majority of questions about how vehicles, pedestrians and transit move through a network, SUMO offers more than most users ever exercise, and the other essays in this folder are meant as a shopping list for that surplus.
