# Common Problems

## Why vehicles teleport

Teleporting is SUMO's way of resolving a **gridlock**, and it is a symptom to investigate rather than a feature to accept. When a vehicle has been waiting longer than `--time-to-teleport` (300 seconds by default), it is removed from its position and reinserted on a later edge of its route, or removed altogether with `--time-to-teleport.remove`. Setting the threshold negative disables the mechanism and lets jams persist, which is sometimes appropriate when diagnosing. Teleport warnings state a reason, and the reasons map onto distinct causes. A **wrong lane** teleport means the vehicle is on a lane with no connection to the next edge of its route, with a shorter timeout on fast roads. A **yield** teleport means a vehicle on a minor road cannot find a gap. A **jam** teleport means that, even with priority, there is no room on the next edge. **Blocked** means the vehicle waits behind a stopped one, and time at scheduled stops does not count. **Disconnected** means that the consecutive route edges are not connected for the vehicle's class, **bidi** means a deadlock on a bidirectional track, and **rail signal** means a circular dependency among trains.

The remedy depends on the reason. Most are fixed by correcting the network (junction priorities, missing lane connections, unjoined junction clusters), by correcting signal plans, by reducing the demand, or by choosing better insertion lanes. A frequent trigger is the combination of a high-density flow with `departLane` defaults, which inserts vehicles on lanes from which their route cannot continue, and `departLane="best"` is the usual fix.

## Unexpected jamming

Persistent jams and deadlocks in a scenario that should flow have five usual causes. The network may be faulty, with wrong lane counts, missing turning lanes, broken connections or junctions that should have been joined. The signal plans may not match the demand. The demand may be excessive overall or concentrated on one edge. The routing may be naive, computing shortest paths without assignment, or may generate many turnarounds. Or vehicles may be inserted onto the wrong lane just before a junction. The practical method is to run in sumo-gui, observe where congestion first appears, and examine the lane connections and signal states there, rather than adjusting global parameters. For OSM networks, applying the recommended import options (joined junctions, guessed ramps and signals) avoids most structural jams.

## Too many turnarounds

Vehicles that have to reverse direction cross all lanes of an intersection and often block it. They arise when routes begin or end on an edge pointing the wrong way or when random demand generation chooses such edges, and they are reduced by routing between junctions or zones, removing route loops in duarouter, and restricting where netconvert creates turnarounds, as covered in [09-traffic-management.md](09-traffic-management.md).

## Unexpected lane-changing manoeuvres

When vehicles change lane late or in strange places, the cause is almost always an **invalid lane-to-lane connection**. The simulator makes drivers change into whichever lane has a connection to the next edge in their route, so a missing or wrongly assigned connection forces a change at the last moment. The way to check is to enable the display of lane-to-lane connections at junctions in sumo-gui and compare it with the intended layout, then correct connections in netedit or in a connections file. The lane-change output can reveal the motivation of each change.

## How to get high flows

A single lane can in principle carry more than 2,500 vehicles per hour, but a default setup achieves less because of insertion and the random slowdown. The recommended insertion settings are `departSpeed="max"`, `departPos="last"` and `departLane="best"`. Further increases need more aggressive vehicle parameters, namely `sigma="0"`, `minGap="1"`, `length="3"` and `tau="0.5"`, and the manual provides a table of insertion capacity for different combinations and step lengths. These changes alter the behaviour, so use them to reproduce observed saturation flows rather than as defaults.

## Performance and reproducibility

A step length of 0.1 seconds is ten times slower than the default of one second, so use fine steps only when the models require them (EIDM, ACC). On Windows the console log buffering can dominate the runtime and is avoided with `--no-step-log`. For very large scenarios the mesoscopic model can be hundreds of times faster. Identical inputs, options and versions give identical results, and variation across runs should be generated deliberately with different seeds.

## Route errors

When routing reports that no connection exists between edges, the reasons are usually invalid permissions for the vehicle class, missing lane connections, or a vehicle class that has no path in a network built for others. The `netcheck.py` tool lists connected components and visualises connectivity problems, and routing with a different vehicle class helps isolate whether permissions are responsible.
