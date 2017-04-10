               __________________________________________

                GTDB (A GRAPHICAL DEBUGGER FOR TORQUE3D)

                   https://gitlab.com/andijh92/gtdb/
               __________________________________________


Table of Contents
_________________

1 About
2 Setup
.. 2.1 on GNU/Linux
.. 2.2 on Windows
3 Quick Start Tutorial





1 About
=======

  GTDB is a graphical debugger for Torque3d (www.torque3d.org), It works
  on GNU/Linux and Windows. It is free/libre software released under the
  GPLv2 licence.

  Currently, the debugger is only tested on GNU/Linux. It is in alpha
  state. It should work, but there may be some issues.

  Philipe Cain is the main author of the debugger.The the development
  stopped in 2008. In 2017 Andreas J. Heil updated the debugger.


2 Setup
=======

  Gtdb has the following prerequisites:
  - Python 2.7
  - wxPython


2.1 on GNU/Linux
~~~~~~~~~~~~~~~~

  You can then install gtdb by invoking:
  $ cd path/to/gtdb-source
  $ ./configure && make && sudo make install

  Start gtdb by invoking:
  $ gtdb

  Alternatively you can start gtdb directly from the source directory by
  invoking.
  $ cd path/to/gtdb-source
  $ ./configure && ./env gtdb/gtdb


2.2 on Windows
~~~~~~~~~~~~~~

  TODO: add documentation


3 Quick Start Tutorial
======================

  You can find a quick start tutorial on the following page:
  [http://eviwo.free.fr/torque/Debugger-documentation.html#Quick_start]
  .
