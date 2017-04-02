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

from gtdb.Parameters import *
from gtdb.Util import *
_ = lang()


class MySplashScreen(wx.SplashScreen):

    def __init__(self):
        gif = image(IMAGE_DEBUGGER)
        wx.SplashScreen.__init__(
            self,
            gif,
            wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
            5000,
            None,
            -1,
            )
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)

    def OnClose(self, evt):

        # Make sure the default handler runs too so this window gets
        # destroyed

        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now

        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        frame = 0
