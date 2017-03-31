"""
Debugger for Torque , more information http://www.garagegames.com/products/torque/tge/.
Copyright (C) 2007  philippe.cain@orange.fr, more information http://eviwo.free.fr/torque/Debugger-documentation.html

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

"""
 constant used by the debugger
"""

import wx
# application directory 
APPLICATION		= 'torqueDebug'
SAVE_APPLIC		=	'connect.txt'
DIR_ICON 			= 'icons'
DIR_LOCALE 		= 'locale'
DIR_LEXER 		= 'lexer'
KEY1					=	'key1.txt'
KEY2					=	'key2.txt'
KEY3					=	'key3.txt'
KEY4					=	'key4.txt'
KEY5					=	'key5.txt'
STYLE					= 'style.txt'

# icon used for the tool bar
ICON_START		= 'Play.png'
ICON_STOP			= 'Stop.png'
ICON_PAUSE		= 'Pause.png'
ICON_STEPIN		= 'StepIn.png'
ICON_STEPOVER = 'StepOver.png'
ICON_RUNCURS	= 'RunToCursor.png'
ICON_STEPOUT	= 'StepOut.png'
ICON_DUMP			= 'Dump.png'
ICON_SAVE			= 'Save.png'

# value used to save the game debug environment
EXT_DEBUG				= '.TDebug'
GAME_DIRECTORY 	= 'directoryGame'
GAME_FILESCRIPT = 'fileScript'
GAME_FILEBINARY	= 'fileBinary'
GAME_FILEUNIX 	= 'fileUnix'
GAME_UNIXPARA 	= 'unixPara'
GAME_PORT 			= 'port'
GAME_PWD 				= 'pwd'
GAME_LOCALHOST 	= 'localhost'
DIR_ENGINE			= 'engine'

# value by default
CONNECT_MAIN		= 'main.cs'
CONNECT_BINARY  = 'torqueDemo_DEBUG.bin'
CONNECT_PARA		= '-nohomedir'
CONNECT_PORT		= "28000"
CONNECT_PWD			= "password"
CONNECT_LOCALH	= "127.0.0.1"

#url
URL='http://eviwo.free.fr/torque/Debugger-documentation.html'

#image
IMAGE_DEBUGGER	= 'debuggerSplash.png'

#report
NOGROUP					= 'ZZZZNoGroup'
NOGROUP_TITLE		= 'Functions without group'
REPORT_OUT			= 'report.html'
REPORT_DIR			= 'report'
REPORT_IN				= 'report-Script.html'
