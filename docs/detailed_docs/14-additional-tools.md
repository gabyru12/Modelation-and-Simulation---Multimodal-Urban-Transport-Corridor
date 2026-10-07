# Additional Tools, Theory and References

## The tool ecosystem

Besides the compiled applications, SUMO ships a large collection of Python scripts in its `tools` directory, organised by purpose. There are groups for traffic assignment, for working with traffic analysis zones, for processing real detector data, for importing external formats (GTFS, MATsim, OSM, OpenDRIVE, Vissim, VISUM), for manipulating networks, for processing simulation output, for railways, routes, shapes and signals, for exporting mobility traces, for turn-count analysis and for visualisation. All of them need Python and the `SUMO_HOME` variable. Their value for a researcher is that nearly every repetitive chore (comparing two networks, extracting a subnetwork, aggregating outputs, generating routes from counts) already has a script that understands SUMO's file formats.

## The web wizard and import scripts

`osmWebWizard.py` is a browser-based scenario generator that turns a selected map region into a runnable simulation, as described in [02-network-building.md](02-network-building.md). It writes all files to a timestamped directory including a build script that regenerates the demand after network edits. `osmGet.py` and `osmBuild.py` handle larger areas by downloading in tiles and building with chosen options.

## sumolib

**sumolib** is the Python library on which most tools are built, and is the natural companion to TraCI for offline work. Its network module reads a compiled network with `sumolib.net.readNet()` and exposes nodes, edges, lanes and connections as objects, with methods for coordinates, successors, lengths and shapes, together with spatial queries such as finding the edges within a radius of a point, which needs the `pyproj` module for geographic conversions. Its XML module parses SUMO's output and input files as streams of attribute-bearing objects, with a fast mode and optional type conversion for attributes, so that a gigabyte-size trip-information file can be processed without loading it into memory. Further modules provide statistics such as medians and quartiles, helpers for writing patched XML files, and miscellaneous geometry and unit functions.

```python
import sumolib
net = sumolib.net.readNet("net.net.xml")
for trip in sumolib.xml.parse("tripinfo.xml", "tripinfo"):
    print(trip.id, float(trip.duration))
```

## XML and conversion tools

Because all SUMO data are XML, a set of generic tools helps analysis. `xml2csv.py` flattens any SUMO XML file into CSV for spreadsheets and pandas, and `csv2xml.py` converts back, `xml2protobuf.py` and `protobuf2xml.py` compress files to Protocol Buffers for size, `changeAttribute.py` adds, modifies or removes attributes throughout a file, and `filterElements.py` deletes elements by attribute conditions. The newer tabular output options often make the conversion step unnecessary.

## Visualisation tools

Matplotlib-based scripts produce standard plots from output files. `plot_trajectories.py` draws time-distance and speed-acceleration plots from FCD output, `plot_summary.py` draws time series from summary output, `plot_net_dump.py` colours a network by edge-based measures such as flow or emissions, `plot_net_selection.py`, `plot_net_speeds.py` and `plot_net_trafficLights.py` annotate the network, `plot_tripinfo_distributions.py` draws histograms of trip data, and `plotXMLAttributes.py` is a flexible tool for line, scatter, box and histogram plots of arbitrary XML attributes. The general CSV plotters handle tabular files.

## Trace export, comparison and utilities

`traceExporter.py` converts FCD output into the trace formats of other simulators and analysis tools, so that SUMO mobility can drive network simulators. `netdiff.py` compares two networks and writes the differences as patch files, which supports versioned network development. Other scripts check connectivity, extract subnetworks, join and split networks, evaluate turn counts, run multiple seeds and generate vehicle type distributions.

## Theory

Traffic simulations are classified into macroscopic models, in which flow is the basic quantity, microscopic models of individual vehicles driven by driver behaviour and vehicle physics, mesoscopic models in which vehicles move between queues, and sub-microscopic models that include internal vehicle details such as engine speed and gear. SUMO is microscopic and, in the sense of spatial representation, space-continuous rather than a cellular automaton in which streets are cells. The behaviour of a driver depends on the distance to the leader and its speed, which defines a car-following model, and its original model is that of Stefan Krauß. Route choice is treated by dynamic user assignment because simultaneous shortest-path choices make congestion worse for everybody.

## Application manuals and appendices

Every program has a manual page listing all its options with types, defaults and descriptions, and these are the authoritative reference once the concepts here are understood: `sumo`, `sumo-gui`, `netconvert`, `netedit`, `netgenerate`, `od2trips`, `duarouter`, `jtrrouter`, `dfrouter`, `marouter`, `polyconvert`, `activitygen`, and the emission tools. The appendices contain the change log, which should be consulted when a default appears to differ from this text, a glossary, the FAQ, a list of file extensions (for example `.net.xml` for networks, `.rou.xml` for routes, `.add.xml` for additional files, `.sumocfg` for configurations) and a complete listing of XML elements and attributes. The contributed-software section lists extensions included in the distribution and external projects, such as co-simulation frameworks, that build on SUMO.
