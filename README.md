<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#org5c0f5b7">1. About</a></li>
<li><a href="#orgabafad4">2. Setup</a>
<ul>
<li><a href="#org371974b">2.1. on GNU/Linux</a></li>
<li><a href="#orgd6c586f">2.2. on Windows</a></li>
</ul>
</li>
<li><a href="#org1d45712">3. Quick Start Tutorial</a></li>
<li><a href="#orga5e82a0">4. Contact</a></li>
<li><a href="#orgc3c4fea">5. News</a></li>
</ul>
</div>
</div>


<a id="org5c0f5b7"></a>

# About

GTDB is a graphical debugger for Torque3d (www.torque3d.org). It works on
GNU/Linux and Windows. It is free/libre software released under the GPLv2
licence. The current version is 0.2.

The debugger is in beta state. There are some tiny issues. Restarting the game
and the debugger often helps.

Philipe Cain is the main author of the debugger. The the development stopped
in 2008. In 2017 Andreas J. Heil updated the debugger.


<a id="orgabafad4"></a>

# Setup

Gtdb has the following prerequisites:  

-   Python 2.7
-   wxPython 3.0

If you compile it from git source on GNU/Linux, you also need:

-   gnu autotools (autoconf, make, automake)
-   autoconf-archive


<a id="org371974b"></a>

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


<a id="orgd6c586f"></a>

## on Windows

You can easily install the prerequisites with the package manager chocolatey. If
you have chocolatey installed, you can run:   
$ choco -y install wxpython

To run gtdb, execute the script in the main gtdb source folder named
"START\_ON\_WINDOWS.py" with python. This may look like that: 'right click on the
file' -> 'open with' -> 'python.exe'


<a id="org1d45712"></a>

# Quick Start Tutorial

You can find a quick start tutorial on the following page: 
<http://eviwo.free.fr/torque/Debugger-documentation.html#Quick_start> .


<a id="orga5e82a0"></a>

# Contact

If you have problems, don't hesitate and write a mail:   
andijh92 @@ gmx DOT at


<a id="orgc3c4fea"></a>

# News

Version 0.3

-   Security issue:

Starting a game with gtdb using a malicious .gtdb file can lead to the execution
of malicious code. Now, there is a warning about that. In the next version of
gtdb you can hide the warning permanently.

Version 0.2

-   Windows support
-   The parameter files have the new extension ".gtdb".

Version 0.1

-   first release

