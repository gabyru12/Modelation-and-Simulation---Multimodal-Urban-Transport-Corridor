# Measurement and Output

## Looking at the same traffic from many angles

SUMO can record the same simulated traffic from the viewpoint of a single vehicle, a single trip, a road segment, a sensor, a whole zone or the entire system, and each viewpoint answers different questions.

From the **vehicle's** own viewpoint, floating-car data gives the full trajectory of every vehicle at every step, with position, speed, angle and type, and can be written in geographic coordinates. Emission output adds pollutant, fuel and electricity values per step. Lane-change output records every manoeuvre and its reason, and collision output records who collided with whom, where and when. A full-output mode writes a very broad state dump for visualisation, and trajectory exports exist in standard and 3D formats and in the formats of other simulators.

From the **trip's** viewpoint, trip information gives each journey's departure and arrival, duration, route length, waiting time, time lost relative to free driving, reroutes and optionally emissions, energy consumption and charging. Route output records the path taken and its costs, stop output records dwell and schedule adherence, and person-related outputs report walking and riding times, waiting and transfers.

From the **road's** viewpoint, edge and lane data aggregate flow, density, speed, occupancy, travel time, waiting time, emissions and noise over chosen intervals and chosen road groups, and queue output estimates tailbacks in front of junctions. Detector files from induction loops, lane-area and multi-entry-exit detectors reproduce field measurements for comparison and calibration.

From the **system's** viewpoint, summary output gives running, waiting, inserted and arrived vehicles and mean speed at each step, and statistic output gives totals such as teleports, collisions, mean delays and travel times. Signal states, signal switches and programs can be logged, and battery and charging output summarise electric fleets.

From the **safety** viewpoint, surrogate safety devices compute time-to-collision, headways and braking rates, and collisions can be detected at junctions and on road segments, with several policies for what happens afterwards.

## Formats and handling

Output is XML by default, but can be written as CSV or Parquet, compressed, sent to a socket or standard output, split by run with timestamps in file names and restricted to selected vehicles, edges or intervals. A set of tools converts XML to CSV and back, filters elements, draws trajectory plots, time-series plots, histograms, network heat maps by any edge measure and signal maps, and exports traces. The graphical interface can colour the network and vehicles by dozens of measures during the run, show detector values, label vehicles and paths and record images or video.
