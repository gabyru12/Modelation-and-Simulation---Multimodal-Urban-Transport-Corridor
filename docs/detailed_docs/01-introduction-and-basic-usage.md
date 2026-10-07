# Introduction and Basic Usage

## What SUMO is

SUMO, the Simulation of Urban MObility, is an open-source traffic simulation package whose defining characteristic is that it is **microscopic**: every vehicle is an explicit object with its own route, its own physical and behavioural parameters, and its own position and speed that are updated step by step. This contrasts with macroscopic tools, which treat traffic as a continuous flow with density and speed fields, and with mesoscopic tools, which move vehicles between queues without resolving their exact positions. The distinction matters for a newcomer because it determines both what SUMO can answer and what it costs. Because vehicles are individual, you can observe queue spillback, lane-changing conflicts, signal-induced shockwaves and the effect of one slow bus on the cars behind it. Because vehicles are individual, runtime also scales with the number of vehicles and with the temporal resolution you request. SUMO is space-continuous, meaning a vehicle's position along a lane is a floating-point number rather than a cell index, and time-discrete, meaning the world is advanced in fixed steps, one second by default.

The project started at the German Aerospace Center in 2000 with the aim of giving transport researchers an open platform on which they could implement and evaluate their own algorithms without first writing a complete simulator. That motivation explains much of the design. The engine is portable standard C++, all data are plain XML, and the simulator is deterministic by default, so that two runs with the same inputs and the same version produce identical results. It is released under the Eclipse Public License 2.0 and hosted under the Eclipse Foundation.

## A suite, not a monolith

The most important architectural decision is that SUMO is a family of small command-line programs that communicate through files, rather than one large application. Network preparation, demand generation, routing and simulation are separate steps with separate tools, each of which can use data structures tuned to its job and each of which can be replaced or extended independently. The core simulator is **sumo** (headless) and **sumo-gui** (the same engine with an OpenGL front end used for inspection and debugging). Networks are produced by **netconvert**, which converts external formats and compiles hand-written XML into the simulator's native network format, by **netgenerate**, which creates abstract grid, spider and random networks, and by **netedit**, a graphical editor built on top of netconvert. Demand is prepared by **duarouter** (shortest and optimal path routing and dynamic user assignment), **jtrrouter** (routing by turning ratios), **dfrouter** (routes from detector counts), **marouter** (macroscopic assignment), **od2trips** (origin-destination matrices to individual trips) and **activitygen** (population-based demand). **polyconvert** imports points of interest and polygons for visual context. A large collection of Python tools sits around these programs, including the **sumolib** library and the **TraCI** client for live control.

The practical consequence for a new user is that a complete scenario is the product of a pipeline. A road network is built once, demand is generated and routed against that network, and the simulator consumes both together with optional infrastructure definitions. Understanding which stage owns which concern prevents a great deal of confusion, for instance why a vehicle that "has a route" can still fail to depart (the route was valid for the network but the vehicle class is not permitted on a lane) or why a signal plan is part of the network rather than the demand.

## Notation and prerequisites

The manual uses a few conventions worth recognising. Angle-bracket words such as `<SUMO_HOME>` denote values you must substitute, ellipses and bracketed fragments denote optional parts, and attribute tables list a default and a permitted range. Distances are in metres, speeds in metres per second, and times in seconds unless a tool states otherwise. The Python tools require Python 3 and an environment variable named `SUMO_HOME` pointing at the installation directory, because the tools locate schemas, typemaps and shared modules through it.

## Installing

SUMO is distributed as Windows installers and portable archives, as Debian and Ubuntu packages, as a Flatpak, as macOS packages, and as Docker images. On Windows the executables live in a `bin` folder inside the installation, and the "extra" builds add GPL-licensed components such as video encoding. Python modules are available from the package index as `eclipse-sumo`, `traci`, `sumolib` and `libsumo`, which is the simplest route for scripting. After installing, set `SUMO_HOME` in the shell profile and install the tool requirements from the `tools` directory so that the visualisation and import scripts have their dependencies.

## Using the command-line applications

Every SUMO program is a plain executable that accepts options in the form `--option value`, `--option=value` or a one-letter abbreviation such as `-n`. Options are typed (integer, float, string, boolean, list) and validated on start-up, lists are comma-separated, and a leading `+` before a list option appends to, rather than replaces, a list given in a configuration file. Because the number of options in the larger programs runs into the hundreds, programs also read **configuration files**, which are XML documents in which each option becomes an element carrying a `value` attribute:

```xml
<configuration>
    <input>
        <net-file value="test.net.xml"/>
        <route-files value="test.rou.xml"/>
    </input>
</configuration>
```

A configuration file is loaded with `-c file.sumocfg` or simply by passing the file name, and the section headings inside it (`input`, `time`, `output`) are only organisational. Command-line values override configuration-file values, with the single exception that `--random` takes precedence over `--seed`. Any program can write out a template of all its options with `--save-template`, write the effective configuration with `--save-configuration`, and emit an XML schema with `--save-schema`; after saving, the program exits rather than running, which surprises many first-time users. Inside configuration files, `${VARNAME}` expands environment variables, and several special names such as `${PID}` and `${LOCALTIME}` are predefined, which is convenient for giving each run in a batch its own output directory.

Output destinations obey a small grammar: a file name writes a file, `stdout` or `-` writes to standard output, a `host:port` pair writes to a socket, and `/dev/null` or `NUL` discards the output. A file name that contains the word `TIME` has it replaced by the start time, and existing files are overwritten silently. Time values are accepted in seconds, `HH:MM:SS` or `DD:HH:MM:SS`, and `--human-readable-time` makes the programs print the same formats.

## Validation and tabular output

Because every input is XML, a misspelt attribute would otherwise be silently ignored. SUMO programs can validate inputs against XML schemas shipped in the installation, controlled by `--xml-validation` with the values `never`, `local`, `auto` and `always`. The default validates routes against locally available schemas but does not validate network files, which are large and machine-generated. A document opts in by declaring its schema in the root element through `xsi:noNamespaceSchemaLocation`; if `SUMO_HOME` is unset, the schema is fetched from the web, which can slow start-up or fail offline.

Most outputs can also be written as CSV or Parquet by choosing the file extension, as in `--fcd-output fcd.parquet`, with the options `--output.format`, `--output.compression`, `--output.column-separator` and `--output.column-header` controlling the details. The documentation measures Parquet files at roughly four-fifths smaller than the equivalent XML and about a hundred times faster to read with pandas, which makes the format attractive for large experiments.

## Tutorials

The official tutorials progress from creating a first network in netedit and importing OpenStreetMap data, through TraCI-controlled traffic lights, to railway scenarios built from OSM and GTFS data and pedestrian scenarios with JuPedSim. The yearly user-conference material from DLR covers topics such as opposite-direction driving, pedestrian crossings and parking search, and is the best source of worked examples for features that the reference pages describe only abstractly.
