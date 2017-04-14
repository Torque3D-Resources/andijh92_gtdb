<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#org6ed9c62">1. About</a></li>
<li><a href="#org0ee1bcf">2. Setup</a>
<ul>
<li><a href="#org1f0d490">2.1. on GNU/Linux</a></li>
<li><a href="#orga37abb9">2.2. on Windows</a></li>
</ul>
</li>
<li><a href="#orge030bfb">3. Quick Start Tutorial</a></li>
<li><a href="#orge628ca8">4. Contact</a></li>
</ul>
</div>
</div>


<a id="org6ed9c62"></a>

# About

GTDB is a graphical debugger for Torque3d (www.torque3d.org). It works on
GNU/Linux and Windows. It is free/libre software released under the GPLv2
licence.

The debugger is in alpha state. There are some tiny issues. Restarting the game
and the debugger often helps.

Philipe Cain is the main author of the debugger. The the development stopped
in 2008. In 2017 Andreas J. Heil updated the debugger.


<a id="org0ee1bcf"></a>

# Setup

Gtdb has the following prerequisites:  

-   Python 2.7
-   wxPython 3.0

If you compile it from git source on GNU/Linux, you also need:

-   gnu autotools (autoconf, make, automake)
-   autoconf-archive


<a id="org1f0d490"></a>

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


<a id="orga37abb9"></a>

## on Windows

You can easily install the prerequisites with the package manager chocolatey. If
you have chocolatey installed, you can run:   
$ choco install wxpython

To run gtdb, execute the script in the main gtdb source folder named
"START\_ON\_WINDOWS.py" with python. This may look like that: 'right click on the
file' -> 'open with' -> 'python.exe'


<a id="orge030bfb"></a>

# Quick Start Tutorial

You can find a quick start tutorial on the following page: 
<http://eviwo.free.fr/torque/Debugger-documentation.html#Quick_start> .


<a id="orge628ca8"></a>

# Contact

If you have problems, don't hesitate and write a mail:   
andijh92 @@ gmx DOT at

