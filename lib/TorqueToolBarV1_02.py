#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import wx

from TorqueParametersV02 import *
from TorqueUtilV03_01 import *
_ = lang()


class Tool(wx.ToolBar):

    def __init__(
        self,
        parent,
        id,
        mainFrame=0,
        ):
        wx.ToolBar.__init__(
            self,
            parent,
            -1,
            (-1, -1),
            (-1, -1),
            wx.TB_DOCKABLE,
            )

        self.mainFrame = mainFrame
        self.SetToolBitmapSize((24, 24))
        self.Tool_Start = self.AddSimpleTool(10, image(ICON_START),
                _('_Start-lib'), _('_Start-libLong'))
        self.Tool_Stop = self.AddSimpleTool(15, image(ICON_STOP),
                _('_Stop-lib'), _('_Stop-libLong'))
        self.Tool_Pause = self.AddSimpleTool(20, image(ICON_PAUSE),
                _('_Pause-lib'), _('_Pause-libLong'))
        self.Tool_StepIn = self.AddSimpleTool(25, image(ICON_STEPIN),
                _('_StepIn-lib'), _('_StepIn-libLong'))
        self.Tool_StepOver = self.AddSimpleTool(30,
                image(ICON_STEPOVER), _('_StepOver-lib'),
                _('_StepOver-libLong'))
        self.Tool_RunCurs = self.AddSimpleTool(35, image(ICON_RUNCURS),
                _('_RunCurs-lib'), _('_RunCurs-libLong'))
        self.Tool_StepOut = self.AddSimpleTool(40, image(ICON_STEPOUT),
                _('_StepOut-lib'), _('_StepOut-libLong'))
        self.Tool_Dump = self.AddSimpleTool(50, image(ICON_DUMP),
                _('_Dump-lib'), _('_Dump-libLong'))
        self.Tool_SaveText = self.AddSimpleTool(45, image(ICON_SAVE),
                _('_Save-lib'), _('_Save-libLong'))  # V2.4

        self.Realize()
        self.enable(False)
        self.enableStart(False)
        self.enableDebug(False)
        self.enableSave(False)  # V2.4

    def enable(self, status):
        self.EnableTool(10, status)
        self.EnableTool(15, status)
        self.EnableTool(20, status)

        # self.EnableTool(25,status)
        # self.EnableTool(30,status)
        # self.EnableTool(35,status)
        # self.EnableTool(40,status)
        # self.EnableTool(50,status)

    def enableStart(self, status):
        self.EnableTool(10, status)

    def enableDebug(self, status):
        self.EnableTool(25, status)
        self.EnableTool(30, status)
        self.EnableTool(35, status)
        self.EnableTool(40, status)
        self.EnableTool(50, status)

    def enableSave(self, status):  # V2.4
        self.EnableTool(45, status)
        self.mainFrame.menu.enableMenuSaveText(status)
