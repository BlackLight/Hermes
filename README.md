[![Build Status](https://travis-ci.org/BlackLight/evesp.svg?branch=master)](https://travis-ci.org/BlackLight/evesp)

Installation
============

    $ git clone https://github.com/BlackLight/evesp
    $ cd evesp/
    $ pip install .

Configuration
=============

By default, the configuration will be retrieved, in order, from one of the
following locations:

1. `./evesp.conf`
2. `~/.config/evesp/evesp.conf`
3. `/etc/evesp/evesp.conf`

An example configuration file is installed under
`~/.config/evesp/evesp.conf.example`.  Sections having `enabled=False` will be
skipped.

Engine
======

    TODO

Components
==========

Components are located under `evesp.component`. A component will usually
install a pool of sockets, poll them for events, and post them to the platform
bus connected to the engine.

Naming convention
-----------------

Lower-case, underscore-separated file names, and camel case name for the
component main class.

Example: `evesp.component.mock_component` will have a main class named
`MockComponent`.  Component classes should extend `evesp.component.Component`,
invoke the base class constructor, and implement the `run()` method.

Sockets
=======

A socket can be installed by a component to generate events that the component
will spawn to the bus. Such events may include:

* INotify file events
* GPS and location events
* Bluetooth events
* Any kind of HTTP requests
* Social media notifications
* Calendar integration
* System-generated events
* IFFF, Tasker etc. events
* Any class of events that pops into your mind with any custom application logic and API.

A component will usually install a bunch of sockets, poll them for events, and
post those events to the platform bus connected to an engine. The engine will
then apply some custom logic on the basis of what is defined in its rules, and
eventually trigger actions based on the received events.

Sockets are installed under `evesp.socket`, implement a `run()` method that
executes the custom logic to generate events, and fire events back to component
calling `fire_events()`.

Actions
=======

    TODO

Tests
=====

    TODO

