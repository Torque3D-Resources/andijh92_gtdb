<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#org078b053">1. About</a></li>
<li><a href="#org1a3cffb">2. Setup</a>
<ul>
<li><a href="#orge24d77a">2.1. on GNU/Linux</a></li>
<li><a href="#orgf30ab98">2.2. on Windows</a></li>
</ul>
</li>
<li><a href="#org95c0bcb">3. Quick Start Tutorial</a></li>
</ul>
</div>
</div>


<a id="org078b053"></a>

# About

GTDB is a graphical debugger for Torque3d (www.torque3d.org), It works on
GNU/Linux and Windows. It is free/libre software released under the GPLv2
licence.

Currently, the debugger is only tested on GNU/Linux. It is in alpha state. There
are some tiny issues. Restarting the game and the debugger often helps.

Philipe Cain is the main author of the debugger.The the development stopped
in 2008. In 2017 Andreas J. Heil updated the debugger.


<a id="org1a3cffb"></a>

# Setup

Gtdb has the following prerequisites:  

-   Python 2.7
-   wxPython 3.0

If you compile it from git source, you also need:

-   gnu autotools (autoconf, make, automake)
-   autoconf-archive

Currently, you can only compile from git source. Windows is not tested yet.


<a id="orge24d77a"></a>

## on GNU/Linux

If you use Ubuntu (16.04) you can fetch the prerequisites with the following
command   
$ sudo apt-get install -y python python-wxgtk3.0 autotools-dev autoconf-archive
make

Compile gtdb with:  
$ cd path/to/gtdb  
$ ./bootstrap && ./configure && make

Start gtdb with:  
$ cd path/to/gtdb  
$ ./env gtdb/gtdb

You can also install it after compilation with:  
$ cd path/to/gtdb  
$ sudo make install

Then you can start it just with:
$ gtdb


<a id="orgf30ab98"></a>

## on Windows

TODO: add me


<a id="org95c0bcb"></a>

# Quick Start Tutorial

You can find a quick start tutorial on the following page: 
<http://eviwo.free.fr/torque/Debugger-documentation.html#Quick_start> .

