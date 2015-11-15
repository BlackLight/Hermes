[![Build Status](https://travis-ci.org/BlackLight/evesp.svg?branch=master)](https://travis-ci.org/BlackLight/evesp)

Installation
============

    $ git clone https://github.com/BlackLight/evesp
    $ cd evesp/
    $ pip install .

Dependencies
------------

PyDispatcher (http://pydispatcher.sourceforge.net/), `pip install PyDispatcher`

Configuration
=============

By default, the configuration will be retrieved, in order, from one of the following locations:

1. `./evesp.conf`
2. `~/.config/evesp/evesp.conf`
3. `/etc/evesp/evesp.conf`

An example configuration file is installed under `~/.config/evesp/evesp.conf.example`.
Sections having `enabled=False` will be skipped.

Components
==========

Components are located under `evesp.component`. Naming convention: lower-case, underscore-separated file names, and camel case name for the component main class.
e.g. `evesp.component.mock_component` will have a main class named `MockComponent`.
Component classes should extend `evesp.component.Component`, invoke the base class constructor, and implement the `run()` method.

