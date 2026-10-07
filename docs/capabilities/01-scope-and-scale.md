# Scope and Scale

## The kinds of questions SUMO is used for

SUMO is a general-purpose microscopic traffic simulator, which means it can be pointed at an unusually broad family of questions. Traffic engineers use it to test signal timings, ramp metering ideas, lane allocations, speed-limit strategies and the effect of closing a street. Transport planners use it to compare route-choice and assignment outcomes, to test public-transport priority and timetable robustness, and to see how a new bike lane or pedestrian zone changes the network. Environmental researchers use it to estimate emissions, fuel use and noise for a fleet and its driving patterns. Vehicle-technology researchers use it as a test bed for adaptive cruise control, platooning, connected-vehicle messages, automated-driving hand-over, charging strategies for electric fleets and on-demand mobility services. Safety researchers use it to measure surrogate safety indicators such as time-to-collision. Machine-learning researchers use it as an environment in which an agent controls signals or vehicles and is rewarded for reducing delay. Because the whole thing is open and scriptable, it is also used simply to generate realistic traffic traces for other simulators.

## Levels of detail

The same input files can be run at different levels of detail. In the default **microscopic** mode every vehicle follows a car-following model and makes its own lane-change and junction decisions, in time steps that can be as coarse as one second or as fine as a millisecond. With the **sublane** option the lane stops being the unit of lateral position, so that bicycles and motorcycles can ride side by side inside one lane and vehicles can nudge around each other. In the **mesoscopic** mode vehicles are moved between queues on road segments, which runs roughly a hundred times faster and suits very large networks or assignment studies. For pedestrians, the lane-based striping model handles sidewalks and crossings, while the JuPedSim coupling provides free-space crowd dynamics in plazas and stations at hundredth-of-a-second resolution. The choice is a dial, and the same scenario can be moved along it as an experiment grows or narrows.

## Spatial and temporal reach

Networks with tens of thousands of edges are routine, and the documentation reports on the order of a hundred thousand vehicle updates per second on modest hardware. A simulation can cover a single intersection for a few minutes, a corridor for a rush hour, a city for a full day, or, with saved states, a long series of experiments that all branch from one warmed-up morning. Time can start at any moment and run for any length, demand can be defined by the hour with day profiles, and the engine can be paused, saved, reloaded or stepped under external control.

## Deterministic yet stochastic

SUMO is deterministic by default, so that the same inputs always give the same result, which is valuable for debugging and for fair comparisons. At the same time it has abundant randomness that can be switched on in a controlled way: driver imperfection, individually drawn speed factors, random departures, mixtures of vehicle types and routes, probabilistic flows and randomly equipped fleets. Running many seeds yields the statistical spread that a serious study needs, and a helper script automates it.

## An ecosystem rather than a program

SUMO ships with more than a dozen programs and a large library of Python tools that import networks and timetables from other formats, convert demand data, compare networks, plot results, export traces and manage experiments. It is open source under the Eclipse Public License, is portable across Windows, Linux and macOS, and uses plain XML for everything, so its data are easy to generate, inspect and transform with ordinary scripting. There are bindings for Python, C++, Java and, experimentally, C# and MATLAB, and an interface that lets outside programs steer the running simulation.
