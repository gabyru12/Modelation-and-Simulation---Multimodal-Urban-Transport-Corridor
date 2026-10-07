# Simulation Output

## The shape of SUMO's output system

SUMO writes nothing unless asked. Output is opt-in, each kind of output has its own option or additional-file element, and outputs differ chiefly in their *granularity* and in *what is aggregated over what*. Understanding that axis is more useful than memorising the list. Some outputs are **disaggregated per vehicle**, recording one entry per vehicle per time step. Others are **aggregated per vehicle**, producing one summary per vehicle trip. Others aggregate over **space and time** for an edge or lane, over a **detector**'s footprint, or over the **whole network** per step. A researcher chooses by asking which question will be asked later: the shape of one vehicle's trajectory, the delay distribution of all trips, the flow on a corridor, or the state of the system as a function of time.

Output is configured either through command-line options such as `--tripinfo-output file.xml` and `--summary-output file.xml` or by declaring elements in an additional file. By default the files are XML, but the extension selects the format: `.csv` and `.parquet` produce tabular output (see [01-introduction-and-basic-usage.md](01-introduction-and-basic-usage.md)), and `.gz` compresses. `--output-prefix` helps separate repeated runs, for example with the start time.

## Per-vehicle trajectory outputs

The most detailed output is **floating-car data** (FCD), which records for every vehicle at every step the position, angle, speed and type, and is the canonical input for trajectory analysis, for visualisation and for exporting to other tools through the trace exporter. **Emission output** records pollutant and fuel values per vehicle per step, and **full output** records a wide variety of edge, lane and vehicle information for building visualisations. The **lane-change output** logs each lane change with its motivation, which is invaluable when diagnosing why vehicles weave. There are also Amitran-standard trajectories, VTK files for 3D tools, and a deprecated raw position dump.

## Per-vehicle aggregate outputs

**Trip information** (`--tripinfo-output`) writes one record per vehicle when it finishes: departure and arrival time, route length, duration, waiting time, time loss relative to driving at the desired speed, number of reroutes and optionally emissions. It is the most commonly used output for evaluating a scenario because delays and times can be aggregated by vehicle type or by departure time afterwards. **Vehicle route output** (`--vehroute-output`) records the edges each vehicle took, the costs at decision time and any rerouting events, which is what you need to analyse route choice. **Stop output** records the start and end of each stop for buses, deliveries and parking, **collision output** records the participants and locations of collisions, and battery output records the energy state of electric vehicles. Persons appear in a restricted set of outputs, namely trip info, route output, FCD, netstate, stop output and mean-data with person detection.

## Edge- and lane-based outputs

**Mean-data** outputs aggregate over a time interval and a set of edges or lanes, producing measures such as mean speed, density, flow, occupancy, travel time, waiting time and sampled seconds, and variants exist for emissions and noise. They produce the same kind of data a macroscopic model produces and are the usual input for travel-time weights in routing and for comparing runs spatially. **Queue output** estimates the actual tailback length in front of a junction per lane and time step.

## Simulated detectors

SUMO reproduces the measurement devices of real traffic engineering. **Induction loops** (E1 detectors) sit at a point on a lane and count vehicles, speeds and occupancy over an aggregation period, and an instantaneous variant records every passing individually. **Lane-area detectors** (E2) cover a stretch of lane and report occupancy, queue length and jam statistics, like a camera. **Multi-entry-exit detectors** (E3) cover an area defined by entry and exit crossing lines and report how long vehicles took to traverse it. Route probes sample route distributions. The mesoscopic engine does not support lane-area or multi-entry-exit detectors.

## System-level outputs

**Summary output** writes, for every time step, the number of loaded, inserted, running, waiting, arrived and teleporting vehicles together with mean speed and waiting time, and so is the standard way to see whether a simulation is stable or has clogged. **Statistic output** writes a final report with totals such as teleports, collisions and mean travel times, and is the best single file to compare many runs. There are also person summaries, and for traffic lights outputs for states, switches and the programs themselves.

## Choosing outputs

A pragmatic rule is to enable summary and statistic output always, trip information for any study of delay, FCD only for short runs or small areas because its volume grows with vehicles times steps, and detector or mean-data outputs when the measurement should correspond to real-world data. Output frequencies, aggregation periods and attribute selections are controlled in the corresponding elements, and writing Parquet when output volume is large saves both disk and analysis time.
