# Libsumo: TraCI Without the Socket

## Motivation

TraCI's client/server design has two costs. Every call crosses a socket, with serialisation and context switches, and the simulation and the controller run as separate processes. For scripts that issue thousands of calls per step, as is typical in reinforcement-learning loops or large co-simulations, the protocol overhead can dominate the runtime. **Libsumo** removes the socket. It is a C++ library exposing the same functions as TraCI as static functions with a few simple result wrapper classes, linked directly into the client program, so that the simulation runs inside the client's own process and a "command" is an ordinary function call.

## Using it

The API deliberately mirrors TraCI, so a script written against TraCI usually needs only a changed import. In Python, after installing the package, `import libsumo as traci` switches an existing script, and setting the environment variable `LIBSUMO_AS_TRACI` makes the standard `traci` import resolve to libsumo without editing the code. `libsumo.start([...])` starts the simulation in-process, `libsumo.simulationStep()` advances it and the domain modules (`vehicle`, `trafficlight`, `edge` and so on) have the same names and signatures as in TraCI.

```python
import libsumo as traci
traci.start(["sumo", "-c", "scenario.sumocfg"])
for _ in range(3600):
    traci.simulationStep()
    n = traci.vehicle.getIDCount()
traci.close()
```

C++ clients link against `libsumocpp` using headers from the installation, Java uses prebuilt bindings (on Windows the native libraries must be preloaded explicitly), C# bindings are generated experimentally with SWIG, and MATLAB reaches libsumo through its Python bridge by prefixing calls with `py.`. A sibling library named **libtraci** exposes an API compatible with libsumo but speaks the TraCI protocol, which lets the same client code run either in-process or against a remote simulation.

## Limitations to know

The trade for speed is flexibility. Libsumo cannot be shared by multiple clients, because there is only one process. Running with the graphical sumo-gui is not supported on Windows and is experimental elsewhere, so visual debugging should be done with TraCI. Subscriptions that need additional arguments are unsupported. Type checking is stricter than in the Python TraCI client, so calls that happen to work through the socket with loosely typed arguments may be rejected. Finally, because the simulation lives in the client's process, a crash in one takes down the other, and parallel simulations in one process are not possible, so parallel experiments should use separate processes. A reasonable workflow is to develop and debug a controller with TraCI and sumo-gui, and then switch to libsumo for large batch runs.
